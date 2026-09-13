// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title ArrowCoreStaking
 * @notice Staking pool for Arrow Core protocol liquidity and privacy rewards
 * Delivers 12.4% annual APY distributed continuously per second.
 */
contract ArrowCoreStaking {
    uint256 public constant APY_BPS = 1240; // 12.4% APY (in basis points, 10000 = 100%)
    uint256 public constant SECONDS_PER_YEAR = 365 days;

    struct StakeInfo {
        uint256 amount;
        uint256 lastClaimTime;
        uint256 rewardDebt;
    }

    mapping(address => StakeInfo) public stakes;
    uint256 public totalStaked;
    uint256 public totalRewardsPaid;

    event Staked(address indexed user, uint256 amount, uint256 timestamp);
    event Unstaked(address indexed user, uint256 amount, uint256 reward, uint256 timestamp);
    event RewardClaimed(address indexed user, uint256 reward, uint256 timestamp);

    error ZeroAmount();
    error InsufficientStake();
    error TransferFailed();

    /**
     * @notice Stake ETH into the pool
     */
    function stake() external payable {
        if (msg.value == 0) revert ZeroAmount();

        StakeInfo storage user = stakes[msg.sender];
        if (user.amount > 0) {
            uint256 pending = calculateReward(msg.sender);
            user.rewardDebt += pending;
        }

        user.amount += msg.value;
        user.lastClaimTime = block.timestamp;
        totalStaked += msg.value;

        emit Staked(msg.sender, msg.value, block.timestamp);
    }

    /**
     * @notice Calculate pending rewards for a user
     */
    function calculateReward(address account) public view returns (uint256) {
        StakeInfo memory user = stakes[account];
        if (user.amount == 0 || user.lastClaimTime == 0) {
            return user.rewardDebt;
        }

        uint256 timeElapsed = block.timestamp - user.lastClaimTime;
        uint256 newReward = (user.amount * APY_BPS * timeElapsed) / (10000 * SECONDS_PER_YEAR);
        return user.rewardDebt + newReward;
    }

    /**
     * @notice Unstake ETH with all accumulated rewards
     * @param amount Amount to unstake
     */
    function unstake(uint256 amount) external {
        StakeInfo storage user = stakes[msg.sender];
        if (amount == 0 || amount > user.amount) revert InsufficientStake();

        uint256 reward = calculateReward(msg.sender);
        user.amount -= amount;
        user.rewardDebt = 0;
        user.lastClaimTime = block.timestamp;
        totalStaked -= amount;
        totalRewardsPaid += reward;

        uint256 totalPayout = amount + reward;
        if (address(this).balance < totalPayout) {
            totalPayout = amount; // fallback to staked amount if pool rewards depleted
        }

        (bool success, ) = msg.sender.call{value: totalPayout}("");
        if (!success) revert TransferFailed();

        emit Unstaked(msg.sender, amount, reward, block.timestamp);
    }

    /**
     * @notice Claim pending rewards only
     */
    function claimReward() external {
        uint256 reward = calculateReward(msg.sender);
        if (reward == 0) revert ZeroAmount();

        StakeInfo storage user = stakes[msg.sender];
        user.rewardDebt = 0;
        user.lastClaimTime = block.timestamp;
        totalRewardsPaid += reward;

        (bool success, ) = msg.sender.call{value: reward}("");
        if (!success) revert TransferFailed();

        emit RewardClaimed(msg.sender, reward, block.timestamp);
    }

    /**
     * @notice Get user staking details
     */
    function getUserInfo(address account) external view returns (
        uint256 stakedAmount,
        uint256 pendingReward,
        uint256 lastStaked
    ) {
        StakeInfo memory user = stakes[account];
        return (user.amount, calculateReward(account), user.lastClaimTime);
    }

    receive() external payable {}
}
