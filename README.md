# Certbot-dns-ovh
Docker container for creating and renewing (wildcard) certificates on OVH DNS

# Building container
To build the container simply run the following command:

```docker build -t certbot-dns-ovh . ```

A ready-made image should be made available soon.

# Create OVH API Token
Go to https://api.ovh.com/createToken/ and create an application token with the following rights:

- For `/domain` verbs *GET, POST, PUT and DELETE* (basically all)
- For `/domain/*` verbs *GET, POST, PUT and DELETE* (basically all)

You should use an OVH account that has the corresponding rights, obviously.

# Running container
The certificate creation and renewal is fully automatic.

You can provide the OVH API credentials using an `ovh.conf` file, as describe in https://github.com/ovh/python-ovh#2-configure-your-application.
You can also use environment variables instead like in the following example:

```docker
docker run -it --rm \
	-v $PWD/certs:/etc/letsencrypt \
	-v $PWD/lib:/var/lib/letsencrypt \
	-e OVH_APPLICATION_KEY=<replace by key> \
	-e OVH_APPLICATION_SECRET=<replace by secret> \
	-e OVH_CONSUMER_KEY=<replace by consumer key> \
	certbot-dns-ovh \
		certonly \
		--server https://acme-v02.api.letsencrypt.org/directory \
		--preferred-challenges dns-01 \
		-a certbot-dns-ovh:dns-ovh \
		--email <your@email.com> \
		--agree-tos \
		--no-eff-email \
		-d "<yourdomain>"
		-d "<yourotherdomain>"
```

To be able to create wildcard certificates you have to use the following endpoint (like in the example above):

`https://acme-v02.api.letsencrypt.org/directory`

# Credit
Inspired by [mcdado/certbot-dns-ovh](https://github.com/mcdado/certbot-dns-ovh) and [antoiner77/letsencrypt.sh-ovh](https://github.com/antoiner77/letsencrypt.sh-ovh)

Copyright (c) 2018, [Weaverize SAS](http://www.weaverize.com). All rights reserved. Contact: <dev@weaverize.com>.
