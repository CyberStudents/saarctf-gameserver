#!/usr/bin/env python3
import os
import sys
import traceback

from sqlalchemy import func

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from saarctf_commons import config

config.EXTERNAL_TIMER = True

"""
Marks a team as "online" for the gameserver. Called as "up" script from OpenVPN.
ARGUMENTS: Team-ID
"""


def main():
	import controlserver.app
	team_id = int(sys.argv[1])
	is_vpn_2 = sys.argv[2] == 'cloudhosted' if len(sys.argv) > 2 else False
	from controlserver.models import Team, db
	if is_vpn_2:
		changes = Team.query.filter(Team.id == team_id).update(dict(vpn2_connected=True, vpn_last_connect=func.now()), synchronize_session=False)
	else:
		changes = Team.query.filter(Team.id == team_id).update(dict(vpn_connected=True, vpn_last_connect=func.now()), synchronize_session=False)
	db.session.commit()
	if changes > 0:
		print(f'Updated connection status (connected) of team #{team_id}.')
	elif team_id > 0:
		if is_vpn_2:
			db.session.add(Team(id=team_id, name=f'unnamed team #{team_id}', vpn2_connected=True, vpn_last_connect=func.now()))
		else:
			db.session.add(Team(id=team_id, name=f'unnamed team #{team_id}', vpn_connected=True, vpn_last_connect=func.now()))
		db.session.commit()
		print(f'Updated connection status (connected) of team #{team_id}. Created new dummy team entry for that.')
	else:
		print(f'Team #{team_id} not found.')


if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		with open('/tmp/connect-error.log', 'a') as f:
			f.write('=== CONNECT ===')
			f.write(repr(sys.argv))
			traceback.print_exc(file=f)
			f.write('\n')
		raise
