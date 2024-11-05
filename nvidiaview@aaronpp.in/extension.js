const St = imports.gi.St;
const Main = imports.ui.main;
const GLib = imports.gi.GLib;
const Gio = imports.gi.Gio;
const Mainloop = imports.mainloop;

let panelButton, panelButtonText, timeout;


function execCommand(argv, input = null, cancellable = null) {
    let cancelId = 0;
    let flags = Gio.SubprocessFlags.STDOUT_PIPE|
        Gio.SubprocessFlags.STDERR_PIPE;

    if (input !== null)
        flags |= Gio.SubprocessFlags.STDIN_PIPE;

    let proc = new Gio.Subprocess({
        argv: argv,
        flags: flags
    });
    proc.init(cancellable);

    if (cancellable instanceof Gio.Cancellable)
        cancelId = cancellable.connect(() => proc.force_exit());

    return new Promise((resolve, reject) => {
        proc.communicate_utf8_async(input, cancellable, (proc_, res) => {
            try {
                let [, stdout, stderr] = proc_.communicate_utf8_finish(res);
                let status = proc_.get_exit_status();

                if (status !== 0) {
                    throw new Gio.IOErrorEnum({
                        code: Gio.io_error_from_errno(status),
                        message: stderr ? stderr.trim() : GLib.strerror(status),
                    });
                }

                resolve(stdout.trim());
            } catch (e) {
                reject(e);
            }
            finally {
                if (cancelId > 0)
                    cancellable.disconnect(cancelId);
            }
        });
    });
}

async function setOutput() {
    try {
        let output = await execCommand(['nvidia-smi','--query-gpu=utilization.memory', '--format=csv,noheader']);
        let prefix = "GPU: ";
        panelButtonText.set_text(prefix + output);
    } catch (e) {
        logError(e);
    }
}

function init() {
    panelButton = new St.Bin({
        style_class: "panel-button"
    });
    panelButtonText = new St.Label({
        text: "GPU: --",
        y_align: St.Align.MIDDLE
    });
    panelButton.set_child(panelButtonText);
}

function enable() {
    Main.panel._rightBox.insert_child_at_index(panelButton, 0);
    timeout = Mainloop.timeout_add_seconds(2, setOutput);
}

function disable() {
    Mainloop.source_remove(timeout);
    Main.panel._rightBox.remove_child(panelButton);
}