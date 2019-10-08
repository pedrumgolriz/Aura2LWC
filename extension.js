// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');
const cp = require('child_process')
const path = require('path')
// this method is called when your extension is activated
// your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
	let disposable = vscode.commands.registerCommand('extension.aura2lwc', (data) => {
		if (data.fsPath.split('/').length > 1) {
			let root = data.fsPath.split('/')[data.fsPath.split('/').length - 2];
			if(root.toLowerCase() === 'aura'){
				let pythonPath = path.resolve(__dirname, "script.pyo");
				cp.exec('python '+pythonPath+' -i '+data.fsPath +' -o '+vscode.workspace.rootPath, (err, stdout, stderr) => {
					//console.log('stdout: ' + stdout);
					//console.log('stderr: ' + stderr);
					if (err) {
						vscode.window.showErrorMessage('Conversion Failed');
						console.log('error: ' + err);
					}
					else{
						console.log("#########OUTPUT###########");
						console.log(stdout);
						vscode.window.showInformationMessage('Conversion Complete');
					}
				});
				//if script returns success
				//else
			}
			else{
				vscode.window.showWarningMessage('Not an Aura Component');
			}
		}
	});

	context.subscriptions.push(disposable);
}
exports.activate = activate;

// this method is called when your extension is deactivated
function deactivate() { }

module.exports = {
	activate,
	deactivate
}
