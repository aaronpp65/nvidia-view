.PHONY: install restart-shell check-deps

check-deps:
	@if ! command -v gnome-extensions >/dev/null; then \
		echo "Installing required package: gnome-shell-extensions..."; \
		sudo apt-get update && sudo apt-get install -y gnome-shell-extensions; \
	fi
	
install:
	@echo "Installing extension..."
	mkdir -p ~/.local/share/gnome-shell/extensions
	cp -r nvidiaview@aaronpp.in ~/.local/share/gnome-shell/extensions/
	@echo "Extension installed. Restarting GNOME Shell..."
	$(MAKE) restart-shell
	@echo "Enabling extension..."
	gnome-extensions enable nvidiaview@aaronpp.in
	@echo "Installation complete"
restart-shell:
	@-pkill -HUP gnome-shell || dbus-send --type=method_call --dest=org.gnome.Shell /org/gnome/Shell org.gnome.Shell.Eval string:'global.reexec_self()' || killall -3 gnome-shell
	@echo "GNOME Shell restart initiated"
	@sleep 2  # Give shell time to restart before enabling extension

	
uninstall:
	@echo "Uninstalling extension..."
	gnome-extensions disable nvidiaview@aaronpp.in
	rm -rf ~/.local/share/gnome-shell/extensions/nvidiaview@aaronpp.in
