# Easygoing - a simple, ~~easy and secure~~ experimental personal blog.
A simple blog I created for my personal needs. May be useful for someone so I put it here. (Contributions welcome!)

## Prerequisites
- Root user on Debian 8 target host.
- Docker installed on local machine.
- Python and Fabric installed on local machine. 

## Installation
Clone the repo and:
```bash
cd easygoing
fab -H root@<target_fqdn> deploy:email=<email>,username=<username> 
```
You will be prompted for password somewhere in the middle.

## TODOs: 
- Verify cron/certbot runs so that certificate can update automatically (saved on a volume).
- Navbar custom image.
- Add favicon (uploadable?).
- Add login rate limit.
- Fix - do not leak information about existing posts (requesting existing but hidden posts redirects to login page).
- (Possibly) Migrate to REST framework. Simplify image/file upload, associate it with posts/sidebar info. 
- (Possibly) Configurable image background and/or styles option (if customization of bootstrap dynamically possible - upload theme.css?).
- (Possibly) Dynamic entries in Navbar.
- (Possibly) Add post author information for multi-author use case.
- (Possibly) Mitigate markdown syntax XSS vulnerabilites, so it can be also used by users.
- (Possibly) Post and Comment should be moved to the same model (tree-like content structure).
- (Possibly) Add entire edit history to model - make everything undeletable.
- (Possibly) Add support for more distros to fabfile.py.
- (Possibly) Add search (haystack?).

## License
This project is licensed under the MIT License - see the LICENSE.md file for details
