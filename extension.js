const vscode = require('vscode');
const fetch = require('node-fetch');
const FormData = require('form-data');

function activate(context) {
  const disposable = vscode.commands.registerCommand(
    'docstringGenerator.generate',
    async () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor) {
        vscode.window.showErrorMessage('No active editor. Open a Python file.');
        return;
      }

      const doc = editor.document;
      if (doc.languageId !== 'python') {
        vscode.window.showWarningMessage('This command works on Python files.');
      }

      const backendUrl = vscode.workspace
        .getConfiguration('docstringGenerator')
        .get('backendUrl') || 'http://127.0.0.1:8000/upload';

      const codeText = doc.getText();
      const filename = require('path').basename(doc.fileName || 'file.py');

      try {
        await vscode.window.withProgress(
          {
            location: vscode.ProgressLocation.Notification,
            title: 'AI Docstring Generator',
            cancellable: false
          },
          async (progress) => {
            progress.report({ message: 'Sending file to backend...' });

            const form = new FormData();
            form.append('file', Buffer.from(codeText, 'utf8'), {
              filename,
              contentType: 'text/x-python'
            });

            const resp = await fetch(backendUrl, {
              method: 'POST',
              body: form
            });

            let data;
            try {
              data = await resp.json();
            } catch (e) {
              throw new Error('Invalid JSON response from backend');
            }

            if (!resp.ok) {
              const detail = (data && data.detail) ? data.detail : resp.statusText;
              throw new Error(`Backend error: ${detail}`);
            }

            const newCode = data.documented_code;
            if (!newCode || typeof newCode !== 'string') {
              throw new Error('Backend returned no documented_code');
            }

            progress.report({ message: 'Applying generated docstrings...' });

            const fullRange = new vscode.Range(
              doc.positionAt(0),
              doc.positionAt(codeText.length)
            );
            const edit = new vscode.WorkspaceEdit();
            edit.replace(doc.uri, fullRange, newCode);
            const applied = await vscode.workspace.applyEdit(edit);

            if (applied) {
              await doc.save();
              vscode.window.showInformationMessage(
                `Docstrings added: ${data.quality_check?.functions_documented ?? 'n/a'} functions`
              );
            } else {
              throw new Error('Failed to apply edit to document');
            }
          }
        );
      } catch (err) {
        vscode.window.showErrorMessage(
          `AI Docstring Generator failed: ${err.message}`
        );
      }
    }
  );

  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate
};

