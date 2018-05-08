# Certbot-dns-ovh
Docker container for creating and renewing (wildcard) certificates on OVH DNS

# Building container
To build the container simply run the following command

```docker build -t certbot-dns-ovh . ```

# Create OVH API Token
Go to https://api.ovh.com/createToken/ and create an application token with the following rights:

- For `/domain` verbs *GET, POST, PUT and DELETE* (basically all)
- For `/domain/*` verbs *GET, POST, PUT and DELETE* (basically all)

You should use an OVH account that has the corresponding rights, obviously.

# Running container
The current POC ask for manual inputs, it will be made fully automatic later on (PR Welcomed ;) )

```docker run -it --rm -v $PWD/certs:/etc/letsencrypt -v $PWD/lib:/var/lib/letsencrypt -e OVH_APPLICATION_KEY=<replace by key> -e OVH_APPLICATION_SECRET=<replace by secret> -e OVH_CONSUMER_KEY=<replace by consumer key> certbot-dns-ovh```

To be able to create wildcard certificates the script uses https://acme-v02.api.letsencrypt.org/directory endpoint.
