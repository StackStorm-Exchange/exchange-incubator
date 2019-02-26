
ST2_EXEC_CMD = grep "execution get" | xargs -0 -I{} bash -c "sleep 2; {}";

run: sync list_repo create_repo get_repo del_repo get_repo list_scripts get_script run_script delete_script get_script test

list_repo:
	echo "=================== List repository"
	st2 action execute nexus3.list_repositories config_profile=dev | grep "execution get" | xargs -0 -I{} bash -c "sleep 2; {}";

create_repo:
	echo "=================== Create repository"
	st2 action execute nexus3.create_repositories config_profile=dev type=hosted name=maven2-dumy format=maven write_policy=ALLOW | $(ST2_EXEC_CMD)

get_repo: 
	echo "=================== Get repository"
	st2 action execute nexus3.get_repositories config_profile=dev name=maven2-dumy | $(ST2_EXEC_CMD)

del_repo:
	echo "=================== Delete repository"
	st2 action execute nexus3.delete_repositories config_profile=dev name=maven2-dumy | $(ST2_EXEC_CMD)

list_scripts:
	echo "=================== List scripts"
	st2 action execute nexus3.list_scripts config_profile=dev | $(ST2_EXEC_CMD)

get_script:
	echo "=================== Get script"
	st2 action execute nexus3.get_scripts config_profile=dev name=nexus3-cli-repository-create | $(ST2_EXEC_CMD)

run_script:
	echo "=================== Run script"
	st2 action execute nexus3.run_scripts config_profile=dev name=nexus3-cli-repository-create | $(ST2_EXEC_CMD)

delete_script:
	echo "=================== Delete script"
	st2 action execute nexus3.delete_scripts config_profile=dev name=nexus3-cli-repository-create | $(ST2_EXEC_CMD)

install:
	echo "=================== Running st2 pack install"
	st2 pack install file://$$PWD

reload: 
	echo "=================== Running st2ctl reload"
	st2ctl reload --register-all

restart:
	echo "=================== Running st2ctl restart"
	st2ctl restart

sync:
	LOCAL_NEXUS_DIR=$$PWD; \
	ST2_PACK_DIR='/opt/stackstorm/packs'; \
	mkdir -p /opt/stackstorm/packs/nexus3; \
	cp -rf $$LOCAL_NEXUS_DIR/*  $$ST2_PACK_DIR/nexus3/; \
	chmod -R --reference $$ST2_PACK_DIR/linux $$ST2_PACK_DIR/nexus3;\
	chown -R --reference $$ST2_PACK_DIR/linux/pack.yaml $$ST2_PACK_DIR/nexus3/*;


lint:
	flake8 ./

validate:
	st2-check-validate-yaml-file ./*.yaml

test:
	st2-run-pack-tests -cjtp ./

