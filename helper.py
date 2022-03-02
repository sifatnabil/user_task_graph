def create_task_triples(data):
    task_triples = []
    project_nodes = []
    board_nodes = []
    card_nodes = []
    task_nodes = []
    software_nodes = []

    user = data['user']
    user_name = user["username"]
    user_email = user["email"]
    user_id = user["id"]

    user_node = (user_id, user_name, user_email)

    projects = data['projects']
    for project in projects:
        project_id, project_name = project['id'], project['name']
        
        project_nodes.append((project_id, project_name))
        task_triples.append((user_name, "has", project_name))

        boards = project['boards']
        for board in boards:
            board_name = board["name"]
            board_nodes.append((board_name,))
            task_triples.append((project_name, "has", board_name))

            cards = board["cards"]
            for card in cards:
                card_name = card["name"]
                card_nodes.append((card_name,))
                task_triples.append((board_name, "has", card_name))

                tasks = card['tasks']
                for task in tasks:
                    task_id = task['id']
                    task_name = task['name']
                    task_time = task['time']
                    task_softwares = task['softwares']
                    task_nodes.append((task_id, task_name, task_time))

                    task_triples.append((card_name, "has", task_name))

                    for software in task_softwares:
                        task_triples.append((task_name, "uses", software))
                        software_nodes.append((software,))


    return user_node, project_nodes, board_nodes, card_nodes, task_nodes, software_nodes, task_triples
    
