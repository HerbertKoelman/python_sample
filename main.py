import utils

if __name__ == '__main__':  # nécessaire que si on veut eviter que ce code soit systématiquement exécuté. Que ce soit comme import ou programme

    print(">>>>>>>>>>>>>>>><  WITH FUNCTIONS\n")

    utils.deploy.artifact('boogla-1.0.0', here='/deploy/here')
    utils.deploy.check_archive_integrity('boolga-1.0.0-x86_64.tar.gz')

    print(">>>>>>>>>>>>>>>><  WITH CLASSES\n")

    ipcm = utils.Artifact('ipcm-1.2.3-snapshot', description="""
This is a very cool thing, crafted by a genius.
    
"Le monde sommeille par manque d'imprudence"
    """)
    print(ipcm.summary())
    utils.PACKAGES.add(ipcm)

    utils.PACKAGES.search_for(utils.Artifact('boogla-1.2.3'))
    utils.PACKAGES.search_for(utils.Artifact('common', version='2.2.1'))
    utils.PACKAGES.search_for(ipcm)


    utils.PACKAGES.deploy(utils.Artifact('common', version='2.2.1'), '/deploy/here')