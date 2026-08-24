calls = [
    {
        "call_id": "CALL-001",

        "customer_name": "John Smith",

        "phone_number": "+91XXXXXXXXXX",

        "agent_name": "Alice",

        "started_at": "2026-08-19T08:00:00Z",

        "duration_seconds": 872,

        "status": "failed",

        "outcome": "unresolved",

        "transcript": (
            "Agent Alice: Hello John, how can I help you today?\n"
            "John Smith: I cannot log in to my account.\n"
            "Agent Alice: Did you receive any error message?\n"
            "John Smith: Yes, the system says my credentials are invalid.\n"
            "Agent Alice: I attempted to help with the login issue, "
            "but the problem could not be resolved during this call.\n"
            "John Smith: I still cannot access my account."
        ),

        "summary": None,

        "notes": [
            {
                "note_id": "NOTE-001",
                "text": "Customer reported login failure.",
                "created_at": "2026-08-19T08:05:00Z",
            },
            {
                "note_id": "NOTE-002",
                "text": "Related job_id: JOB-101",
                "created_at": "2026-08-19T08:10:00Z",
            },
        ],
    },

    {
        "call_id": "CALL-002",

        "customer_name": "Sarah Patel",

        "phone_number": "+91XXXXXXXXXX",

        "agent_name": "Bob",

        "started_at": "2026-08-19T08:20:00Z",

        "duration_seconds": 435,

        "status": "completed",

        "outcome": "resolved",

        "transcript": (
            "Agent Bob: Hello Sarah, how can I help you?\n"
            "Sarah Patel: I forgot my account password.\n"
            "Agent Bob: I can help you reset it.\n"
            "Sarah Patel: Yes, please.\n"
            "Agent Bob: The password reset has been completed.\n"
            "Sarah Patel: I can log in now. Thank you."
        ),

        "summary": None,

        "notes": [
            {
                "note_id": "NOTE-003",
                "text": "Password reset completed successfully.",
                "created_at": "2026-08-19T08:26:00Z",
            },
        ],
    },

    {
        "call_id": "CALL-003",

        "customer_name": "David Shah",

        "phone_number": "+91XXXXXXXXXX",

        "agent_name": "Alice",

        "started_at": "2026-08-19T08:30:00Z",

        "duration_seconds": 1060,

        "status": "failed",

        "outcome": "escalated",

        "transcript": (
            "Agent Alice: Hello David, what seems to be the problem?\n"
            "David Shah: The application keeps crashing when I open it.\n"
            "Agent Alice: Did you recently install any updates?\n"
            "David Shah: Yes, the application was updated yesterday.\n"
            "Agent Alice: I tried the standard troubleshooting steps, "
            "but the application is still crashing.\n"
            "David Shah: So what should I do now?\n"
            "Agent Alice: I will escalate this issue to the technical team."
        ),

        "summary": None,

        "notes": [
            {
                "note_id": "NOTE-004",
                "text": "Technical issue could not be resolved.",
                "created_at": "2026-08-19T08:40:00Z",
            },
            {
                "note_id": "NOTE-005",
                "text": "Related job_id: JOB-103",
                "created_at": "2026-08-19T08:45:00Z",
            },
        ],
    },

    {
        "call_id": "CALL-004",

        "customer_name": "Priya Mehta",

        "phone_number": "+91XXXXXXXXXX",

        "agent_name": "Charlie",

        "started_at": "2026-08-19T09:00:00Z",

        "duration_seconds": 310,

        "status": "completed",

        "outcome": "resolved",

        "transcript": (
            "Agent Charlie: Hello Priya, how can I help you?\n"
            "Priya Mehta: I was unable to update my profile information.\n"
            "Agent Charlie: Let me check your account.\n"
            "Agent Charlie: The issue has been corrected.\n"
            "Priya Mehta: I can update my profile now. Thank you."
        ),

        "summary": None,

        "notes": [
            {
                "note_id": "NOTE-006",
                "text": "Issue resolved during the call.",
                "created_at": "2026-08-19T09:04:00Z",
            },
        ],
    },

    {
        "call_id": "CALL-005",

        "customer_name": "Michael Patel",

        "phone_number": "+91XXXXXXXXXX",

        "agent_name": "Bob",

        "started_at": "2026-08-19T09:10:00Z",

        "duration_seconds": 1160,

        "status": "failed",

        "outcome": "unresolved",

        "transcript": (
            "Agent Bob: Hello Michael, how can I help you?\n"
            "Michael Patel: I cannot access my account.\n"
            "Agent Bob: Have you tried resetting your password?\n"
            "Michael Patel: Yes, but I still cannot log in.\n"
            "Agent Bob: I checked the account and attempted "
            "several troubleshooting steps.\n"
            "Michael Patel: I still cannot access my account.\n"
            "Agent Bob: The issue will require further investigation."
        ),

        "summary": None,

        "notes": [
            {
                "note_id": "NOTE-007",
                "text": "Customer still cannot access account.",
                "created_at": "2026-08-19T09:20:00Z",
            },
            {
                "note_id": "NOTE-008",
                "text": "Related job_id: JOB-105",
                "created_at": "2026-08-19T09:25:00Z",
            },
        ],
    },
    {
        "call_id": "CALL-101",
        "customer_name": "Raj Patel",
        "phone_number": "+91XXXXXXXXXX",
        "agent_name": "Alice",
        "started_at": "2026-08-20T08:00:00Z",
        "duration_seconds": 720,
        "status": "failed",
        "outcome": "unresolved",
        "transcript": (
            "Agent Alice: Hello Raj, how can I help you today?\n"
            "Raj Patel: My refrigerator is running but it is not cooling properly.\n"
            "Agent Alice: Is the refrigerator receiving power?\n"
            "Raj Patel: Yes, the lights are working and I can hear the compressor.\n"
            "Agent Alice: Did you try adjusting the temperature?\n"
            "Raj Patel: Yes, but it is still not getting cold.\n"
            "Agent Alice: I tried the standard troubleshooting steps, "
            "but the cooling issue could not be resolved during the call.\n"
            "Raj Patel: Please arrange a technician visit."
        ),
        "summary": None,
        "notes": [
            {
                "note_id": "NOTE-101",
                "text": "Customer reported refrigerator cooling problem.",
                "created_at": "2026-08-20T08:10:00Z",
            },
            {
                "note_id": "NOTE-102",
                "text": "Related job_id: JOB-011",
                "created_at": "2026-08-20T08:12:00Z",
            },
        ],
    },

    {
        "call_id": "CALL-102",
        "customer_name": "Neha Shah",
        "phone_number": "+91XXXXXXXXXX",
        "agent_name": "Bob",
        "started_at": "2026-08-20T09:00:00Z",
        "duration_seconds": 845,
        "status": "failed",
        "outcome": "unresolved",
        "transcript": (
            "Agent Bob: Hello Neha, how can I help you?\n"
            "Neha Shah: My microwave turns on but it does not heat the food.\n"
            "Agent Bob: Does the microwave display work normally?\n"
            "Neha Shah: Yes, the display and buttons are working.\n"
            "Agent Bob: Does the turntable rotate when you start it?\n"
            "Neha Shah: Yes, it rotates, but the food stays completely cold.\n"
            "Agent Bob: I attempted the available troubleshooting steps, "
            "but the heating problem remains unresolved.\n"
            "Neha Shah: Please arrange a technician to inspect it."
        ),
        "summary": None,
        "notes": [
            {
                "note_id": "NOTE-103",
                "text": "Microwave powers on but does not heat food.",
                "created_at": "2026-08-20T09:12:00Z",
            },
            {
                "note_id": "NOTE-104",
                "text": "Related job_id: JOB-012",
                "created_at": "2026-08-20T09:15:00Z",
            },
        ],
    },

    {
        "call_id": "CALL-103",
        "customer_name": "Amit Mehta",
        "phone_number": "+91XXXXXXXXXX",
        "agent_name": "Charlie",
        "started_at": "2026-08-20T10:00:00Z",
        "duration_seconds": 930,
        "status": "failed",
        "outcome": "escalated",
        "transcript": (
            "Agent Charlie: Hello Amit, what seems to be the problem?\n"
            "Amit Mehta: My washing machine is making a very loud noise "
            "during the spin cycle.\n"
            "Agent Charlie: Does the machine complete the washing cycle?\n"
            "Amit Mehta: Yes, but the noise becomes very loud when it starts spinning.\n"
            "Agent Charlie: Did you check whether the machine is placed on a level surface?\n"
            "Amit Mehta: Yes, it is properly positioned.\n"
            "Agent Charlie: I tried the standard troubleshooting procedure, "
            "but the unusual noise is still present.\n"
            "Amit Mehta: I think a technician needs to inspect the machine.\n"
            "Agent Charlie: I will escalate the issue for a technician visit."
        ),
        "summary": None,
        "notes": [
            {
                "note_id": "NOTE-105",
                "text": "Washing machine produces unusual noise during spin cycle.",
                "created_at": "2026-08-20T10:15:00Z",
            },
            {
                "note_id": "NOTE-106",
                "text": "Related job_id: JOB-013",
                "created_at": "2026-08-20T10:18:00Z",
            },
        ],
    },

    {
        "call_id": "CALL-104",
        "customer_name": "Priya Desai",
        "phone_number": "+91XXXXXXXXXX",
        "agent_name": "Alice",
        "started_at": "2026-08-20T11:00:00Z",
        "duration_seconds": 680,
        "status": "failed",
        "outcome": "follow_up_required",
        "transcript": (
            "Agent Alice: Hello Priya, how can I help you?\n"
            "Priya Desai: My water purifier is not working properly.\n"
            "Agent Alice: What problem are you experiencing?\n"
            "Priya Desai: The purifier is making a strange noise and the water flow is very slow.\n"
            "Agent Alice: When was the filter last replaced?\n"
            "Priya Desai: I am not sure, it has been quite some time.\n"
            "Agent Alice: The issue may require filter replacement and a complete service.\n"
            "Priya Desai: Can someone come and service the purifier?\n"
            "Agent Alice: I could not complete the service remotely, "
            "so I will arrange a technician follow-up."
        ),
        "summary": None,
        "notes": [
            {
                "note_id": "NOTE-107",
                "text": "Water purifier requires service and possible filter replacement.",
                "created_at": "2026-08-20T11:10:00Z",
            },
            {
                "note_id": "NOTE-108",
                "text": "Related job_id: JOB-014",
                "created_at": "2026-08-20T11:12:00Z",
            },
        ],
    },
    {
        "call_id": "CALL-51",
        "customer_name": "Rajesh Kumar",
        "phone_number": "+91-9876543210",
        "agent_name": "Priya",
        "started_at": "2026-08-21T08:30:00Z",
        "duration_seconds": 480,
        "status": "pending",
        "outcome": None,
        "transcript": (
            "Agent Priya: Hello, how can I help you today?\n"
            "Rajesh Kumar: My refrigerator is not cooling. The temperature inside is too warm.\n"
            "Agent Priya: How long has this been happening?\n"
            "Rajesh Kumar: For the past 2 days. I'm worried the food will spoil.\n"
            "Agent Priya: Let me create a service request for you. A technician will visit soon."
        ),
        "summary": None,
        "notes": [
            {
                "note_id": "NOTE-151",
                "text": "Customer reports refrigerator not cooling for 2 days",
                "created_at": "2026-08-21T08:35:00Z",
            },
        ],
    },
    {
        "call_id": "CALL-52",
        "customer_name": "Anjali Singh",
        "phone_number": "+91-9123456789",
        "agent_name": "Vikram",
        "started_at": "2026-08-21T09:15:00Z",
        "duration_seconds": 720,
        "status": "completed",
        "outcome": "follow_up_required",
        "transcript": (
            "Agent Vikram: Good morning, what's the issue?\n"
            "Anjali Singh: My washing machine is making a loud grinding noise during the spin cycle.\n"
            "Agent Vikram: That sounds like a motor issue. Have you tried stopping it midway?\n"
            "Anjali Singh: Yes, but it still makes the noise.\n"
            "Agent Vikram: I recommend a technician visit to check the motor. We can schedule that.\n"
            "Anjali Singh: Okay, but I need it fixed urgently as I have lots of laundry to do.\n"
            "Agent Vikram: Understood, I'll escalate this as urgent."
        ),
        "summary": None,
        "notes": [
            {
                "note_id": "NOTE-152",
                "text": "Washing machine motor grinding noise during spin",
                "created_at": "2026-08-21T09:20:00Z",
            },
            {
                "note_id": "NOTE-153",
                "text": "Customer urgent - has laundry backlog",
                "created_at": "2026-08-21T09:25:00Z",
            },
        ],
    },
    {
        "call_id": "CALL-53",
        "customer_name": "Amit Patel",
        "phone_number": "+91-8765432109",
        "agent_name": "Charlie",
        "started_at": "2026-08-21T10:00:00Z",
        "duration_seconds": 600,
        "status": "pending",
        "outcome": None,
        "transcript": (
            "Agent Charlie: Hello, welcome to service center. What can I help?\n"
            "Amit Patel: My microwave stopped heating food. It just spins but doesn't heat.\n"
            "Agent Charlie: When did this start?\n"
            "Amit Patel: About a week ago. I've been using the oven instead.\n"
            "Agent Charlie: I understand. Let me book a service visit for you.\n"
            "Amit Patel: How soon can someone come?\n"
            "Agent Charlie: We can arrange a visit within 2-3 days."
        ),
        "summary": None,
        "notes": [
            {
                "note_id": "NOTE-154",
                "text": "Microwave not heating - heating element likely faulty",
                "created_at": "2026-08-21T10:05:00Z",
            },
        ],
    },
    {
        "call_id": "CALL-54",
        "customer_name": "Deepika Sharma",
        "phone_number": "+91-7654321098",
        "agent_name": "Diana",
        "started_at": "2026-08-21T11:30:00Z",
        "duration_seconds": 900,
        "status": "completed",
        "outcome": "follow_up_required",
        "transcript": (
            "Agent Diana: Hi Deepika, how are you?\n"
            "Deepika Sharma: Hi, I need AC installation. We just moved to a new house.\n"
            "Agent Diana: Congratulations! What capacity do you need?\n"
            "Deepika Sharma: A 2-ton split AC for the master bedroom.\n"
            "Agent Diana: We have good options. Would you like a quote?\n"
            "Deepika Sharma: Yes, and I need installation this weekend if possible.\n"
            "Agent Diana: Let me check availability and I'll call you back with options."
        ),
        "summary": None,
        "notes": [
            {
                "note_id": "NOTE-155",
                "text": "New customer - 2 ton split AC needed for bedroom",
                "created_at": "2026-08-21T11:40:00Z",
            },
            {
                "note_id": "NOTE-156",
                "text": "Follow-up: Send quote and check weekend installation availability",
                "created_at": "2026-08-21T11:45:00Z",
            },
        ],
    },
    {
        "call_id": "CALL-55",
        "customer_name": "Rohan Gupta",
        "phone_number": "+91-6543210987",
        "agent_name": "Ethan",
        "started_at": "2026-08-21T14:00:00Z",
        "duration_seconds": 420,
        "status": "failed",
        "outcome": "escalated",
        "transcript": (
            "Agent Ethan: Hello, this is technical support.\n"
            "Rohan Gupta: My dishwasher is not draining water. It's a critical issue.\n"
            "Agent Ethan: I understand. Let me troubleshoot with you.\n"
            "Rohan Gupta: I've already tried basic troubleshooting. It's serious.\n"
            "Agent Ethan: In that case, I need to escalate this to a senior technician.\n"
            "Rohan Gupta: How long will that take?\n"
            "Agent Ethan: They'll contact you within 2 hours."
        ),
        "summary": None,
        "notes": [
            {
                "note_id": "NOTE-157",
                "text": "Dishwasher drainage blocked - escalated to senior tech",
                "created_at": "2026-08-21T14:05:00Z",
            },
            {
                "note_id": "NOTE-158",
                "text": "Related job_id: JOB-55",
                "created_at": "2026-08-21T14:08:00Z",
            },
        ],
    },
    {
        "call_id": "CALL-56",
        "customer_name": "Priya Verma",
        "phone_number": "+91-5432109876",
        "agent_name": "Fiona",
        "started_at": "2026-08-21T15:30:00Z",
        "duration_seconds": 540,
        "status": "pending",
        "outcome": None,
        "transcript": (
            "Agent Fiona: Good afternoon! What brings you here today?\n"
            "Priya Verma: I need a ceiling fan installed in my new office.\n"
            "Agent Fiona: Great! What type of fan are you looking for?\n"
            "Priya Verma: Something modern and energy-efficient. I have two rooms.\n"
            "Agent Fiona: I can help with that. We offer professional installation too.\n"
            "Priya Verma: When can you install them?\n"
            "Agent Fiona: Let me check our schedule and get back to you with availability."
        ),
        "summary": None,
        "notes": [
            {
                "note_id": "NOTE-159",
                "text": "Ceiling fan installation needed for 2 office rooms",
                "created_at": "2026-08-21T15:35:00Z",
            },
        ],
    },
]