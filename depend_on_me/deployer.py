import depend_on_me, argparse, sys

if __name__ == '__main__':  # nécessaire que si on veut eviter que ce code soit systématiquement exécuté. Que ce soit comme import ou programme
    """Handles the deployment of artifacts."""

    parser = argparse.ArgumentParser(
        prefix_chars='-',
        description='deploy/install the requirements found in each given YAML file'
    )

    try:

        args = argv_argc.deployment(parser)

        print("deploy artifacts found in {} here {}".format(args.files, args.install_dir))

        if args.install_dir is not None and args.force:
            depend_on_me.utils.remove_all_artifacts_found(args.install_dir)

        for file in args.files:
            print("-------------- ", file, " -----------------")
            for artefact in depend_on_me.load_requirements_from(file):
                depend_on_me.install_package(artefact, arch=args.target_arch, here=args.install_dir )

    except Exception as err:
        print("error: {} failed. {}".format(parser.prog, err))
        sys.exit(-99)
