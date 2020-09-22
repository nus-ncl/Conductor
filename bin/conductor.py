#!/usr/bin/python3

# Standard packages
import sys

# Internal packages
import cli
import user_commands

debug = 0

if __name__ == '__main__':


	# Try except to catch keyboard interrupts
	try:
		cli.print_banner()
		while True:

			cmd = cli.input_with_prompt(cli.Conductor_PROMPT)
			cmdarray = cmd.split()

			if len(cmdarray) == 0:
				print("Type 'help' for usage. 'exit' to quit.")

			if len(cmdarray) != 0:
				if cli.commands.get(cmdarray[0], None) is not None:
					cli.commands[cmdarray[0]](cmdarray[1:])
					continue

			if len(cmdarray) == 1:
				if cmdarray[0] == 'help' or cmdarray[0] == 'h':
					cli.print_help()
				elif cmdarray[0] == 'exit':
					exit(0)
				else:
					print("Type 'help' for usage. 'exit' to quit.")

			if len(cmdarray) == 2:
				if cmdarray[0] == 'help' and cli.commands.get(cmdarray[1], None) is not None:
					user_commands.help_command(cli.commands[cmdarray[1]])
				else:
					cli.print_help()

			if len(cmdarray) > 2:
				print("Type 'help' for usage. 'exit' to quit.")

	except KeyboardInterrupt:
		print("\n\n" + cli.color("^C.   Quitting...", warning=True))
		sys.exit()
	except EOFError:
		print("\n\n" + cli.color("^D.   Quitting...", warning=True))
		sys.exit()
