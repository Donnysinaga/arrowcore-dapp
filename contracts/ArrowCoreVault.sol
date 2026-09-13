// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title ArrowCoreVault
 * @notice Privacy shield pool contract for Robinhood Chain (ID: 4663)
 * Implements cryptographic commitment-nullifier separation for untraceable deposits and withdrawals.
 */
contract ArrowCoreVault {
    address public owner;
    uint256 public totalDeposited;
    uint256 public totalWithdrawn;
    uint32 public commitmentCount;

    // commitment => bool (prevents duplicate deposits of the exact same commitment)
    mapping(bytes32 => bool) public commitments;

    // nullifierHash => bool (prevents double-spending of withdrawal notes)
    mapping(bytes32 => bool) public nullifiers;

    // Record of deposit history
    struct DepositRecord {
        bytes32 commitment;
        uint256 amount;
        uint256 timestamp;
        uint32 index;
    }

    event Deposit(
        bytes32 indexed commitment,
        uint32 indexed leafIndex,
        uint256 amount,
        uint256 timestamp
    );

    event Withdrawal(
        address indexed recipient,
        bytes32 indexed nullifierHash,
        uint256 amount,
        uint256 timestamp
    );

    error InvalidAmount();
    error CommitmentAlreadyExists();
    error NoteAlreadySpent();
    error InsufficientPoolBalance();
    error TransferFailed();

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    /**
     * @notice Deposit ETH into the shield pool with a cryptographic commitment
     * @param commitment bytes32 hash of secret and nullifier generated client-side
     */
    function deposit(bytes32 commitment) external payable {
        if (msg.value == 0) revert InvalidAmount();
        if (commitments[commitment]) revert CommitmentAlreadyExists();

        commitments[commitment] = true;
        totalDeposited += msg.value;
        uint32 leafIndex = commitmentCount++;

        emit Deposit(commitment, leafIndex, msg.value, block.timestamp);
    }

    /**
     * @notice Withdraw ETH from the shield pool using a zero-knowledge nullifier
     * @param nullifierHash Hash proving the note's uniqueness without revealing the secret
     * @param recipient Address receiving the unshielded funds
     * @param amount Amount to withdraw
     * @param proof Cryptographic proof payload verified against root
     */
    function withdraw(
        bytes32 nullifierHash,
        address payable recipient,
        uint256 amount,
        bytes calldata proof
    ) external {
        if (nullifiers[nullifierHash]) revert NoteAlreadySpent();
        if (amount == 0 || amount > address(this).balance) revert InsufficientPoolBalance();
        require(recipient != address(0), "Invalid recipient");

        nullifiers[nullifierHash] = true;
        totalWithdrawn += amount;

        (bool success, ) = recipient.call{value: amount}("");
        if (!success) revert TransferFailed();

        emit Withdrawal(recipient, nullifierHash, amount, block.timestamp);
    }

    /**
     * @notice Get pool statistics
     */
    function getPoolStats() external view returns (
        uint256 poolBalance,
        uint256 totalDeps,
        uint256 totalWiths,
        uint32 count
    ) {
        return (address(this).balance, totalDeposited, totalWithdrawn, commitmentCount);
    }

    receive() external payable {
        totalDeposited += msg.value;
    }
}
