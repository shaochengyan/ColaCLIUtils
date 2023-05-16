from core.ColaCMDMenu import MenuItemSet
import subprocess
import yaml



class KeyFuncClass:
    def __init__(self, session_dict) -> None:
        self.session_dict = session_dict

    def __call__(self):
        for exe, filelist in self.session_dict.items():
            for file in filelist:
                # subprocess.Popen([exe, "", file], shell=True) # return a object to control subprocess and not control.
                if exe == "explorer":
                    subprocess.Popen(['explorer', file])
                elif exe == "web":
                    subprocess.call(["start", "microsoft-edge:"+file], shell=True)  # start microsoft-edge:https://www.example.com
                elif exe == "default":
                    subprocess.Popen(["start", file], shell=True)    
                else:
                    subprocess.Popen([exe, "", file], shell=True) # return a object to control subprocess and not control.
    

class ColaSessions(MenuItemSet):
    def __init__(self, config_session) -> None:
        super().__init__(is_page_dif_prefix=False)

        cmd_dict = dict()
        for name, value in config_session.items():
            description = value["description"]
            session_dict = value["session_dict"]
            cmd_dict[name] = [description, self.gen_keyfunc(session_dict)]
        self.add_menuAkeyfunc(
            "SESSIONS", 
            **cmd_dict
        )    

    def gen_keyfunc(self, session_dict: dict):
        return KeyFuncClass(session_dict)

if __name__=="__main__":
    def get_api_key():
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        return config
    config = get_api_key()
    sess = ColaSessions(config_session=config["Session"])
    sess.runloop()


"""
python -m plugins.Sessions.ColaSessions
"""