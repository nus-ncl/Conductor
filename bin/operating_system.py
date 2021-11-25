os = {
	'node': {
		'Linux': {
			'ubuntu': {
				'16.04': {
					'i386': None,
					'amd64': 'Ubuntu1604-64-STD'
				}
			},
			'centos': {},
			'redhat': {}
		},
		'Windows': {
			'win7': {},
			'ptq': {},
			'xhq': {},
		},
		'Darwin': {
			'test': {}
		}
	},
	'virtualbox': {
		'Linux': {
			'ubuntu': {
				'19': {
					'32': None,
					'64': 'generic/ubuntu1910'
				},
				'16': {
					'32': None,
					'64': 'bento/ubuntu-16.04'
				}
			},
			'centos': {},
			'redhat': {}
		},
		'Windows': {
			'windows': {
				'10': {
					'64': 'gusztavvargadr/windows-10-enterprise'
				}
			},
		},
		'Darwin': {
			'test': {}
		}
	},
	'docker': {
		'Linux': {
			'ubuntu': {
				'20.04': {
					'i386': 'i386/ubuntu:20.04',
					'amd64': 'amd64/ubuntu:20.04'
				},
				'16.04': {
					'i386': 'i386/ubuntu:16.04',
					'amd64': 'amd64/ubuntu:16.04'
				}
			},
			'centos': {},
			'redhat': {}
		},
		'Windows': {
			'win7': {},
			'ptq': {},
			'xhq': {},
		},
		'Darwin': {
			'test': {}
		}
	}
}
