from modules import script_callbacks
from modules import shared
import threading
import time, os

CLIENT_ID = '1065987911486550076'

def check_deps():
    from launch import is_installed, run_pip
    if not is_installed("pypresence"):
        print("Installing the missing 'pypresence' package and its dependencies,")
        print("In case it gave a package error after the installation, restart the webui.")
        run_pip("install pypresence", "pypresence")

def start_rpc():
    from pypresence import Presence
    
    print('Starting Discord RPC extension')
    RPC = Presence(CLIENT_ID)
    RPC.connect()
    
    state_watcher = threading.Thread(target=check_progress_loop, args=(RPC,), daemon=True)
    state_watcher.start()
    print("Done! If everything is fine, the RPC should be running by now.")
    
def on_ui_tabs():
    start_rpc()
    return []

check_deps()
script_callbacks.on_ui_tabs(on_ui_tabs)

# Dynamic status check
def check_progress_loop(RPC,):
    while True:
        checkpoint_info = shared.sd_model.sd_checkpoint_info
        model_name = os.path.basename(checkpoint_info.filename)
        if shared.state.job_count == 0:
            RPC.update(large_image="auto", details="Waiting for user input...", state="Idle.")
        else:
            RPC.update(large_image="generating", details=f"Generating {shared.state.job_count} Picture(s) using '{model_name}' model", state=f'{shared.state.sampling_step}/{shared.state.sampling_steps} Sampling Steps, {shared.state.job_no + 1}/{shared.state.job_count} Jobs in total')
        time.sleep(10) # update every 10 seconds.
