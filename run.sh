#!/bin/sh
if [ -z "$OVH_ENDPOINT" ]
then
	echo "using \"ovh-eu\" as OVH_ENDPOINT"
	export OVH_ENDPOINT=ovh-eu
fi

if [ -z "$OVH_APPLICATION_KEY" ]
then
	echo "please set env var OVH_APPLICATION_KEY"
	exit 1
fi

if [ -z "$OVH_APPLICATION_SECRET" ]
then
	echo "please set env var OVH_APPLICATION_SECRET"
	exit 1
fi

if [ -z "$OVH_CONSUMER_KEY" ]
then
	echo "please set env var OVH_CONSUMER_KEY"
	exit 1
fi

certbot certonly --server https://acme-v02.api.letsencrypt.org/directory --preferred-challenges dns-01 --manual --manual-auth-hook ./manual-auth-hook.py --manual-cleanup-hook ./manual-cleanup-hook.py
