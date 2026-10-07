---
title: Big Data System Lab Note
ai: translated
date: 2023-10-09
lastMod: 2023-10-09
tags:
- Hadoop
- java
categories:
slug: big-data-lab
---

### Set up Hadoop environment

[Apache Hadoop 3.3.6 – Hadoop: Setting up a Single Node Cluster.](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html)


### set up java environment

java version requirements:

[https://cwiki.apache.org/confluence/display/HADOOP/Hadoop+Java+Versions](https://cwiki.apache.org/confluence/display/HADOOP/Hadoop+Java+Versions)

```
% curl -sL "https://builds.openlogic.com/downloadJDK/openlogic-openjdk/8u382-b05/openlogic-openjdk-8u382-b05-linux-x64.tar.gz" -o ./openjdk-8u382.tar.gz
% tar -xvf ./openjdk-8u382.tar.gz
% mv ./openlogic-openjdk-8u382-b05-linux-x64 ./usr/bin/openjdk-8u832
% sudo vim ~/.zshrc
```

add java to path:

```
# ~/.zshrc

#...
export JAVA_PATH="/usr/bin/openjdk-8u832/bin"
export PATH=$PATH:$JAVA_PATH
```

test path:

```
% source ~/.zshrc
% java -version                                                             1 ↵
openjdk version "1.8.0_382-382"
OpenJDK Runtime Environment (build 1.8.0_382-382-b05)
OpenJDK 64-Bit Server VM (build 25.382-b05, mixed mode)
```

### requisite software

`ssh` required, `pdsh` for better performance.

```
% sudo apt install ssh
% sudo apt install pdsh
```

### download hadoop

(switch to a mirror if download is too slow)

```
% curl -LO "https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz" -o ./
% tar -xvf ./hadoop-3.3.6.tar.gz
% sudo mv ./hadoop-3.3.6 /usr/local/bin/hadoop-3.3.6
```

### prepare to start the Hadoop Cluster

edit `hadoop-3.3.6/etc/hadoop/hadoop-env.sh`. Hadoop will try to execute`$JAVA_HOME/bin/java`.

```
# etc/hadoop/hadoop-env.sh

# export JAVA_HOME=$JAVA_PATH/.. 
# The above works when test bin/hadoop, but fails in start-dfs.sh. idk why.
# related: https://stackoverflow.com/questions/40831151/hadoop-cannot-start-start-dfs-sh

export JAVA_HOME=/usr/bin/openjdk-8u832
```

Then try the following command, it will display the doc of hadoop script.

```
% bin/hadoop

Usage: hadoop [OPTIONS] SUBCOMMAND [SUBCOMMAND OPTIONS]
or    hadoop [OPTIONS] CLASSNAME [CLASSNAME OPTIONS]
where CLASSNAME is a user-provided Java class

OPTIONS is none or any of:
...
```

**Execute `hadoop-env.sh` so that `$JAVA_HOME` is exported.**

### Pseudo-Distributed Operation

Use the following:

etc/hadoop/core-site.xml:

```
<configuration>
  <property>
      <name>fs.defaultFS</name>
      <value>hdfs://localhost:9000</value>
  </property>
</configuration>
```

etc/hadoop/hdfs-site.xml:

```
<configuration>
  <property>
      <name>dfs.replication</name>
      <value>1</value>
  </property>
</configuration>
```

### set up passphraseless ssh

```
% ssh localhost
```

If you cannot ssh to localhost without a passphrase, execute the following commands:

```
% ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
% cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
% chmod 0600 ~/.ssh/authorized_keys
```

### yarn on single note

Format the filesystem

```
% bin/hdfs namenode -format
```

try to start NameNode daemon and DataNode daemon, error will be raised:

```
[hadoop@VM7617-BDS-Lab:/usr/local/bin/hadoop-3.3.6]
% sbin/start-dfs.sh                                                         3 ↵
Starting namenodes on [localhost]
pdsh@VM7617-BDS-Lab: localhost: rcmd: socket: Permission denied
Starting datanodes
pdsh@VM7617-BDS-Lab: localhost: rcmd: socket: Permission denied
Starting secondary namenodes [VM7617-BDS-Lab]
pdsh@VM7617-BDS-Lab: VM7617-BDS-Lab: rcmd: socket: Permission denied
[hadoop@VM7617-BDS-Lab:/usr/local/bin/hadoop-3.3.6]
% sudo sbin/start-dfs.sh
Starting namenodes on [localhost]
ERROR: Attempting to operate on hdfs namenode as root
ERROR: but there is no HDFS_NAMENODE_USER defined. Aborting operation.
Starting datanodes
ERROR: Attempting to operate on hdfs datanode as root
ERROR: but there is no HDFS_DATANODE_USER defined. Aborting operation.
Starting secondary namenodes [VM7617-BDS-Lab]
ERROR: Attempting to operate on hdfs secondarynamenode as root
ERROR: but there is no HDFS_SECONDARYNAMENODE_USER defined. Aborting operation.
```

according to [this post on Stackoverflow](https://stackoverflow.com/questions/60181800/some-problems-in-installing-hadoop-error-attempting-to-operate-on-hdfs-namenode), add these lines to `etc/hadoop/hadoop-env.sh`

```
#
# To prevent accidents, shell commands be (superficially) locked
# to only allow certain users to execute certain subcommands.
# It uses the format of (command)_(subcommand)_USER.
#
# For example, to limit who can execute the namenode command,
export HDFS_NAMENODE_USER=hadoop
export HDFS_DATANODE_USER=hadoop
export HDFS_SECONDARYNAMENODE_USER=hadoop
export YARN_RESOURCEMANAGER_USER=hadoop
export YARN_NODEMANAGER_USER=hadoop
```

[sockets - Permission Denied error while running start-dfs.sh - Stack Overflow](https://stackoverflow.com/questions/42756555/permission-denied-error-while-running-start-dfs-sh) - This post explains how pdsh causes the first permission denied problem. Thus we should add an env to zshrc / bashrc / ...:

```
# ~/.zshrc

export PDSH_RCMD_TYPE=ssh
```

Now it works:

```
% sbin/start-dfs.sh
Starting namenodes on [localhost]
Starting datanodes
Starting secondary namenodes [VM7617-BDS-Lab]
VM7617-BDS-Lab: Warning: Permanently added 'vm7617-bds-lab' (ED25519) to the list of known hosts.
```

Check the web interface at `http://localhost:9870`.

Make the HDFS dir required to execute MapRecuce jobs.

```
% bin/hdfs dfs -mkdir -p /user/hadoop
```
