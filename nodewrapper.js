const { execSync } = require('child_process');
const path = require('path');
const core = require('@actions/core');

// Get the artifact-path input from the action
const artifactPath = core.getInput('artifact-path');

if (!artifactPath) {
    core.setFailed('Artifact Path is not defined.');
    process.exit(1);
}

// Define the path to the ts.py script
const scriptPath = path.join(__dirname, 'scripts', 'ts.py');

try {
    // Execute the ts.py script using the provided artifactPath as an argument
    const output = execSync(`python3 ${scriptPath} --xml_directory ${artifactPath}`).toString();
    console.log(output);
    core.setOutput('result', output);
} catch (error) {
    console.error(`Error executing ts.py script: ${error}`);
    core.setFailed(`Error executing ts.py script: ${error.message}`);
    process.exit(1);
}
