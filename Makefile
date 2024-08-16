install:
	mkdir -p ~/.local/share/gnome-shell/extensions
	cp -r nvidiaview@aaronpp ~/.local/share/gnome-shell/extensions/
	
uninstall:
	rm -rf ~/.local/share/gnome-shell/extensions/nvidiaview@aaronpp
