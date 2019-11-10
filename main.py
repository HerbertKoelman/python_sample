import utils

if __name__ == '__main__':  # nécessaire que si on veut eviter que ce code soit systématiquement exécuté. Que ce soit comme import ou programme
    print("Hello, python world...")
    utils.deploy.artifact('boogla-1.0.0', here='/deploy/here')
    utils.deploy.check_archive_integrity('boolga-1.0.0-x86_64.tar.gz')

    boogla = utils.Artifact('boogla-1.2.3')
    print ("Artefact: " , boogla, "Id: ", boogla.id())

    boogla_package = utils.Package(boogla)
    common_package = utils.Package(utils.Artifact('common', version='2.2.1'))
    print (boogla_package)
    print (common_package)

    PACKAGES_HOME='/share/modules'
    packages = utils.Packages(PACKAGES_HOME)
    packages.search_for(boogla_package)