const fs = require('fs');
const path = require('path');
const solc = require('solc');

function compileContract(fileName, contractName) {
    const filePath = path.join(__dirname, 'contracts', fileName);
    const source = fs.readFileSync(filePath, 'utf8');

    const input = {
        language: 'Solidity',
        sources: {
            [fileName]: {
                content: source,
            },
        },
        settings: {
            optimizer: {
                enabled: true,
                runs: 200,
            },
            outputSelection: {
                '*': {
                    '*': ['abi', 'evm.bytecode.object'],
                },
            },
        },
    };

    console.log(`Compiling ${fileName}...`);
    const output = JSON.parse(solc.compile(JSON.stringify(input)));

    if (output.errors) {
        let hasError = false;
        output.errors.forEach(err => {
            console.error(err.formattedMessage);
            if (err.severity === 'error') hasError = true;
        });
        if (hasError) process.exit(1);
    }

    const contract = output.contracts[fileName][contractName];
    const abi = contract.abi;
    const bytecode = contract.evm.bytecode.object;

    return { abi, bytecode };
}

const vault = compileContract('ArrowCoreVault.sol', 'ArrowCoreVault');
const staking = compileContract('ArrowCoreStaking.sol', 'ArrowCoreStaking');
const swap = compileContract('ArrowCoreSwap.sol', 'ArrowCoreSwap');

fs.mkdirSync(path.join(__dirname, 'build'), { recursive: true });

fs.writeFileSync(
    path.join(__dirname, 'build', 'ArrowCoreVault.json'),
    JSON.stringify(vault, null, 2)
);

fs.writeFileSync(
    path.join(__dirname, 'build', 'ArrowCoreStaking.json'),
    JSON.stringify(staking, null, 2)
);

fs.writeFileSync(
    path.join(__dirname, 'build', 'ArrowCoreSwap.json'),
    JSON.stringify(swap, null, 2)
);

// Generate JS bundle
const bundleJs = `// Auto-generated Arrow Core Smart Contract Artifacts
window.ARROW_CONTRACTS = {
    Vault: ${JSON.stringify(vault)},
    Staking: ${JSON.stringify(staking)},
    Swap: ${JSON.stringify(swap)}
};
`;

fs.writeFileSync(path.join(__dirname, 'contracts-bundle.js'), bundleJs);

console.log('Compilation successful! Generated build/ and contracts-bundle.js with Vault, Staking, and Swap!');
