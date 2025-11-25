from random import randint, choice

standart = {
    "name": "standart Level",
    "description": "This is a test level",
    "units": [
        {
            "traits": {
                "trait_a": {"value": 4, "income": 1.0},
                "trait_b": {"value": 4, "income": 2.0},
                "trait_c": {"value": 4, "income": 3.0},
                "trait_d": {"value": 4, "income": 4.0},
                "trait_e": {"value": 4, "income": 5.0},
            },
            "draggedable": True,
            "income_time": 0,
            "life_time": 0,
            "x": 1,
            "y": 1,
            "body_radius": 5.0,
            "aura_radius": 7.0,
        }
    ],
    "timer": 300,
    "goal_score": 100,
    "default_traits_pool": {
        "trait_a": {
            0: {"income": 1.0},
            1: {"income": 1.0},
            2: {"income": 1.0},
            3: {"income": 1.0},
            4: {"income": 1.0},
        },
        "trait_b": {
            0: {"income": 1.0},
            1: {"income": 1.0},
            2: {"income": 1.0},
            3: {"income": 1.0},
            4: {"income": 1.0},
        },
        "trait_c": {
            0: {"income": 1.0},
            1: {"income": 1.0},
            2: {"income": 1.0},
            3: {"income": 1.0},
            4: {"income": 1.0},
        },
        "trait_d": {
            0: {"income": 1.0},
            1: {"income": 1.0},
            2: {"income": 1.0},
            3: {"income": 1.0},
            4: {"income": 1.0},
        },
        "trait_e": {
            0: {"income": 1.0},
            1: {"income": 1.0},
            2: {"income": 1.0},
            3: {"income": 1.0},
            4: {"income": 1.0},
        },
    },
}

lite = {
    "name": "lite Level",
    "units": [{}],
    "goal_score": 100,
}

complicated = {
    "name": "Complicated Level",
    "description": "This is a test level",
    "units": [
        {
            "traits": {
                "trait_a": {},
                "trait_b": {"value": 4},
                "trait_c": {"income": 1.0},
                "trait_e": {"value": 4, "income": 1.0},
            },
            "draggedable": True,
            "income_time": 0,
            "life_time": 0,
            "x": 50,
            "y": 50,
            "body_radius": 5.0,
            "aura_radius": 7.0,
        }
    ],
    "timer": 300,
    "goal_score": 100,
    "default_traits_pool": {
        "trait_a": {
            0: {"income": 1.0},
            4: {},
        },
        "trait_b": {
            0: {"income": 1.0},
            1: {"income": 1.0},
            2: {"income": 1.0},
            3: {"income": 1.0},
            4: {"income": 1.0},
        },
    },
    "income": 0.0,
    "starting_score": 0.0,
}

b = {
    "name": {"type": str, "required": True},
    "description": {"type": str, "required": False, "default": ""},
    "timer": {"type": (int, float), "required": False, "default": float("+inf")},
    "goal_score": {"type": (int, float), "required": True},
    "units": {
        "type": list,
        "required": True,
        "min_length": 1,
        "schema": {
            "draggedable": {"type": bool, "required": False, "default": True},
            "income_time": {"type": (int, float), "required": False, "default": 0.0},
            "life_time": {
                "type": (int, float),
                "required": False,
                "default": float("+inf"),
            },
            "x": {"type": (int, float), "required": False, "default": 0.0},
            "y": {"type": (int, float), "required": False, "default": 0.0},
            "body_radius": {"type": (int, float), "required": False, "default": 5},
            "aura_radius": {"type": (int, float), "required": False, "default": 7},
            "traits": {
                "type": dict,
                "required": False,
                "schema": {
                    "trait_a": {
                        "type": dict,
                        "required": False,
                        "schema": {
                            "value": {
                                "type": int,
                                "required": False,
                                "default": "RANDOM_OPTION",
                            },
                            "income": {
                                "type": float,
                                "required": False,
                                "default": 1.0,
                            },
                        },
                    },
                    "trait_b": {
                        "type": dict,
                        "required": False,
                        "schema": {
                            "value": {
                                "type": int,
                                "required": False,
                                "default": "RANDOM_OPTION",
                            },
                            "income": {
                                "type": float,
                                "required": False,
                                "default": 1.0,
                            },
                        },
                    },
                    "trait_c": {
                        "type": dict,
                        "required": False,
                        "schema": {
                            "value": {
                                "type": int,
                                "required": False,
                                "default": "RANDOM_OPTION",
                            },
                            "income": {
                                "type": float,
                                "required": False,
                                "default": 1.0,
                            },
                        },
                    },
                    "trait_d": {
                        "type": dict,
                        "required": False,
                        "schema": {
                            "value": {
                                "type": int,
                                "required": False,
                                "default": "RANDOM_OPTION",
                            },
                            "income": {
                                "type": float,
                                "required": False,
                                "default": 1.0,
                            },
                        },
                    },
                    "trait_e": {
                        "type": dict,
                        "required": False,
                        "schema": {
                            "value": {
                                "type": int,
                                "required": False,
                                "default": "RANDOM_OPTION",
                            },
                            "income": {
                                "type": (int, float),
                                "required": False,
                                "default": 0,
                            },
                        },
                    },
                },
            },
        },
    },
    "default_traits_pool": {"type": dict, "required": False, "schema": {"trait_a": {}}},
}
