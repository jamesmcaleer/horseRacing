import pygame
import random
import math
import time

pygame.init()



WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SCREEN_X = 1700
SCREEN_Y = int(SCREEN_X * (9/16))
SCREEN_SIZE = (SCREEN_X, SCREEN_Y)

screen = pygame.display.set_mode(SCREEN_SIZE)

clock = pygame.time.Clock()

pygame.display.set_caption("Horse Racing")


FINISH_DISTANCE = 100
SIZE_FACTOR = round(SCREEN_X / 650)
DISTANCE_FACTOR = SIZE_FACTOR * 4
CAMERA_SPEED_OFFSET = 1.5

BACKGROUND = pygame.transform.scale(pygame.image.load(f"assets/background.jpg").convert(), (SCREEN_X * 2,SCREEN_Y))
FINISH_LINE = pygame.image.load(f"assets/finish_line.png").convert_alpha()
FINISH_LINE = pygame.transform.scale(FINISH_LINE, (round(FINISH_LINE.get_width() * 1.5 * SCREEN_X / 1920),round(FINISH_LINE.get_height() * 1.5 * SCREEN_X / 1920)))

PODIUM = pygame.image.load(f"assets/podium.png").convert_alpha()
PODIUM = pygame.transform.scale(PODIUM, (round(PODIUM.get_width() * 0.75 * SCREEN_X / 1920),round(PODIUM.get_height() * 0.75 * SCREEN_X / 1920)))

FIRST_NAMES = ["Aston", "Bearwood", "Cosmic", "American", "French", "English", "Irish", "German", "Italian", "Queen", "King", "Mister", "Salty", "Jazzy", "Uncle", "Saint", "Mountain", "Chief", "Flying", "Solar", "Speedy", "Holy", "Magic", "Sir", "Small", "Golden", "Silver", "Bronze", "Platinum", "Copper", "Crystal", "Dark", "Light", "Bright", "Black", "White", "Fast", "Cranky", "Spooky"]
LAST_NAMES = ["Warrior", "Intruder", "Chariot", "Bullet", "Wanderer", "Champion", "Rocket", "Express", "Cruiser", "Dreamer", "Stormer", "Explorer", "Stallion", "Joker", "Monster", "Fighter", "Master", "Angel", "Gift", "Animal", "Apache", "Breeze", "Cloud", "Dancer", "Eclipse", "Flash", "Fairy", "Hero", "Knight", "Lightning", "Moon", "Victor", "Star", "Thunder", "Ruby", "Gem", "Universe", "Clown", "Jester"]

DARK_BROWN= []
for i in range(9):
    DARK_BROWN.append(pygame.transform.scale(pygame.image.load(f"assets/dark_brown_{i+1}.png").convert_alpha(), (130 *SIZE_FACTOR,75*SIZE_FACTOR)))

LIGHT_BROWN= []
for i in range(9):
    LIGHT_BROWN.append(pygame.transform.scale(pygame.image.load(f"assets/light_brown_{i+1}.png").convert_alpha(), (130*SIZE_FACTOR, 80 *SIZE_FACTOR)))

GRAY = []
for i in range(9):
    GRAY.append(pygame.transform.scale(pygame.image.load(f"assets/gray_{i+1}.png").convert_alpha(), (130*SIZE_FACTOR, 80 *SIZE_FACTOR)))


WHITE_FUR = []
for i in range(9):
    WHITE_FUR.append(pygame.transform.scale(pygame.image.load(f"assets/white_{i+1}.png").convert_alpha(), (130*SIZE_FACTOR, 80 *SIZE_FACTOR)))


OUTLINES = []
for i in range(8):
    OUTLINES.append(pygame.transform.scale(pygame.image.load(f"assets/outline_{i + 1}.png").convert_alpha(), (29*SIZE_FACTOR,20*SIZE_FACTOR)))


CLOTHING_COLOR_IMAGES = []
for i in range(8):
    CLOTHING_COLOR_IMAGES.append(pygame.transform.scale(pygame.image.load(f"assets/color_{i + 1}.png").convert_alpha(), (27*SIZE_FACTOR,16*SIZE_FACTOR)))

DECALS = []
for i in range(8):
    DECALS.append(pygame.transform.scale(pygame.image.load(f"assets/decal_{i + 1}.png").convert_alpha(), (27*SIZE_FACTOR,16*SIZE_FACTOR)))




class ChanceHandler:
    def __init__(self):
        self.all_graphs = []
        self.horse_skeletons = []
        self.odds = []
        

    def generate_odds(self):
        self.odds = []
        remaining = 1
        bottom_bound = 2
        top_bound = 6
        for i in range(8):
            # pick random vals on the bounds and assign an odd
            # take away from the remaining var
            if i == 7:
                odd = round(1 / (2 * remaining))
                self.odds.append((odd, (1, int(remaining * 100))))
            else:
                odd = random.randint(bottom_bound // remaining, top_bound // remaining)

                if any(odd == t[0] for t in self.odds):
                    while any(odd == t[0] for t in self.odds):
                        odd += 1
                takeoff = 1 / (2 * odd)
                temp = remaining
                remaining -= takeoff
                #print(takeoff)
                remaining = round(remaining,2)
                self.odds.append((odd, (int(remaining * 100) + 1, int(temp * 100))))
            
            print(remaining)
            
            # append to odds
        print(self.odds)

        # made odds for 8 horses, make sure the pie chart is full
        # meaning that there should be 100%, one horse gets 25% of the pie, another 5%, but it should add to 100
    
    def sort_speeds(self):
        temp = []
        for i in range(8):
            min_time_index = 0
            for j in range(len(self.all_graphs)):
                if self.all_graphs[j]['finish'] < self.all_graphs[min_time_index]['finish']:
                    min_time_index = j
            temp.append(self.all_graphs[min_time_index])
            self.all_graphs.pop(min_time_index)
        self.all_graphs = temp
        #print(self.all_graphs)
            
    def generate_speeds(self):
        self.all_graphs = []
        # generate 8 different speed graphs
        for g in range(8):
            graph_values = []
            graph = {'finish': 30}
            speed = 4
            distance = 0
            done = False
            for t in range (0, 300):
                time = round(t/10, 1)
                change = random.randint(0, 3) / 10
                flip = random.randint(1,2)
                if flip == 1:
                    if speed - change > 0.5:
                            speed -= change
                    else:
                        speed += change
                else:
                    speed += change

                distance += speed * 0.1
                if distance >= FINISH_DISTANCE and not done:
                    graph['finish'] = time
                    done = True

                speed = round(speed, 1)
                distance = round(distance, 1)
                
                graph_values.append(speed)


                    
            graph['values'] = graph_values

            
            self.all_graphs.append(graph)

        self.sort_speeds()
        
        # how to represent the speed graphs
        # we are running at 10 fps so graph should iterate by 0.1 seconds, 200 data points for 20 seconds

        # how we randomly generate the graphs
        # remember that these graphs dont tie to specific horses yet, we dont need to attach the odds to the random fluctuation in speed**
        # for each graph, start at a random speed from (0,-)
        # every 0.1 second we pick a small amount ex.(0.5, 3) then flip a coin for it to be pos or neg, then we add or sub this to the speed
        # as we are generating, we should keep a running count of the area under the curve/distance traveled
        # if dist > finish dist, we lock in the time they finished
        # graph = {'arr' : values, 'finish time' : time}

        # all_graphs = [{}, {}, ...]

        # using the odds, give fair but random rankings between the horses
        # attach these respective speed graphs to the horses
        
    
        
    

class Leaderboard:
    def __init__(self, actionHandler):
        self.actionHandler = actionHandler
        self.ranking = list(self.actionHandler.horses)

    def adjust_ranking(self):
        temp = []
        for i in range(8):
            min_distance_index = 0
            for j in range(len(self.ranking)):
                if self.ranking[j].body.x < self.ranking[min_distance_index].body.x:
                    min_distance_index = j
            temp.append(self.ranking[min_distance_index])
            self.ranking.pop(min_distance_index)
        self.ranking = list(temp)


class ActionHandler:
    def __init__(self, chanceHandler):
        self.chanceHandler = chanceHandler
        self.horses = []
        self.ranked_horses = []

    def generate_new_horses(self):
        print("generating new horses...")
        self.horses = []
        self.numbered_horses = []
        
        self.chanceHandler.generate_odds()
        self.generate_empties() # empty is a full horse with no speed graph

        self.new_winner()
        
    
    def generate_empties(self): # create the actual horses and attach the odds
        available_numbers = [1,2,3,4,5,6,7,8]
        available_clothing_colors = [0, 1, 2, 3, 4, 5, 6, 7]
        available_fur_colors = [DARK_BROWN, DARK_BROWN, LIGHT_BROWN, LIGHT_BROWN, GRAY, GRAY, WHITE_FUR, WHITE_FUR]

        for i in range(8):
            horse_number = available_numbers.pop(random.randint(0, len(available_numbers)-1))
            horse_clothing_color = available_clothing_colors.pop(random.randint(0, len(available_clothing_colors)-1))
            horse_fur_color = available_fur_colors.pop(random.randint(0, len(available_fur_colors)-1))

            self.horses.append(self.horse_init(self.chanceHandler.odds[i], horse_number, horse_clothing_color, horse_fur_color))

        

        
    
    def apply_speeds(self):
        temp_graphs = list(self.chanceHandler.all_graphs)
        temp_horses = list(self.horses)
        # all_graphs is now sorted
        # pick a number 1-100
        # find which tuple it falls inside of
        # assign the [0] item in all_graphs to the odds tuple
        for i in range(8):
            found = False
            range_index = 0
            while not found:
                random_number = random.randint(1, 100)
                for j in range(len(temp_graphs)):
                    if random_number >= temp_horses[j].odds[1][0] and random_number <= temp_horses[j].odds[1][0]:
                        range_index = j
                        found = True
                        #print('found')
                        break
                    else:
                        #print("couldent find.. restarting")
                        pass
            #print(temp_odds)
            #print('rand', random_number)
            #print('index', range_index)

            temp_horses[j].apply_new_result(temp_graphs[0]['finish'], temp_graphs[0]['values'])
            #temp_horses[j].print_items()
            temp_horses.pop(range_index)
            
            temp_graphs.pop(0)

    def new_winner(self):
        print("generating new winner...")
        self.chanceHandler.generate_speeds() # these two steps can be repeated for replayability
        self.apply_speeds()

        print("before ranking")
        for horse in self.horses:
            horse.print_items()
        # self.chanceHandler.generate_speeds() will come later on
        # also function to apply the speeds to the horses
        
        self.sort_horses_by_time()
        
        print("after ranking")
        for horse in self.ranked_horses:
            horse.print_items()

        self.end_time = self.ranked_horses[0].finish_time * 10
        self.horses = self.sort_horses_by_number()

    def reset_horse_positions(self):
        for horse in self.horses:
            horse.body.x = round(SCREEN_X // 6)

    def sort_horses_by_number(self):
        temp = list(self.horses)
        self.numbered_horses = []
        for i in range(8):
            min_number_index = 0
            for j in range(len(temp)):
                if temp[j].number < temp[min_number_index].number:
                    min_number_index = j
            self.numbered_horses.append(temp.pop(min_number_index))
        return self.numbered_horses

    def sort_horses_by_time(self):
        self.ranked_horses = []
        temp = list(self.horses)
        for i in range(8):
            min_time_index = 0
            for j in range(len(temp)):
                if temp[j].finish_time < temp[min_time_index].finish_time:
                    min_time_index = j
            self.ranked_horses.append(temp.pop(min_time_index))

    def horse_init(self, odds, number, clothing, fur):
        horse = Horse(self, odds, number, clothing, fur)
        # horse.print_items()
        return horse

class Horse:
    def __init__(self, actionHandler, odds, number, clothing, fur, graph=None, finish_time=None, name=None, decal_image=None):
        self.actionHandler = actionHandler
        self.odds = odds
        self.number = number
        self.color = clothing

        self.graph = graph
        self.finish_time = finish_time

        self.body = pygame.Rect((SCREEN_X // 3,0), (10, 50))
        
        self.name = name if name is not None else FIRST_NAMES[random.randint(0, len(FIRST_NAMES)-1)] + " " + LAST_NAMES[random.randint(0, len(FIRST_NAMES)-1)]
        self.number_image = OUTLINES[self.number - 1]
        self.clothing_color_image = CLOTHING_COLOR_IMAGES[self.color]
        self.fur_color = fur
        self.decal_image = decal_image if decal_image is not None else DECALS[random.randint(0, len(DECALS)-1)]

    

    def move(self, time):
        self.body.move_ip(round(((self.graph[time] - CAMERA_SPEED_OFFSET) * 0.1) * DISTANCE_FACTOR), 0)

    def print_items(self):
        print(f'name: {self.name} number {self.number} odds {self.odds[0]}:1, finish_time: {self.finish_time} seconds')

    def apply_new_result(self, finish_time, graph):
        self.finish_time = finish_time
        self.graph = graph

class FinishLine:
    def __init__(self, actionHandler):
        self.actionHandler = actionHandler
        self.real_end = FINISH_DISTANCE * DISTANCE_FACTOR
        self.camera_end_offset = round(CAMERA_SPEED_OFFSET * self.actionHandler.end_time * 0.1 * DISTANCE_FACTOR)
        self.start_offset = SCREEN_X // 6

        self.finish_line_position = self.real_end - self.camera_end_offset + self.start_offset

        travel_distance = SCREEN_X - self.finish_line_position
        travel_time = round(travel_distance / (SCREEN_X // 60))
        self.start_time = self.actionHandler.end_time - travel_time
        self.movement_speed = -1 * SCREEN_X // 60

        self.body = pygame.Rect(SCREEN_X, round(SCREEN_Y / 3) + 5 * SIZE_FACTOR, 2 * SIZE_FACTOR, SCREEN_Y - (round(SCREEN_Y / 3) + 5 * SIZE_FACTOR))
        self.image_hidden = True
    
    def move(self, time):
        if time >= self.start_time:
            self.body.move_ip(self.movement_speed, 0)
            if self.image_hidden:
                self.image_hidden = False

class Podium:
    def __init__(self, actionHandler):
        self.actionHandler = actionHandler
        self.body = pygame.Rect(SCREEN_X - PODIUM.get_width(), SCREEN_Y // 2 - PODIUM.get_height() // 2, PODIUM.get_width(), PODIUM.get_height())

    def horse_podium(self):
        podium_horses = self.actionHandler.ranked_horses[:3]
        for i in range(3):

            copy = podium_horses[i]
            horse = Horse(copy.actionHandler, copy.odds, copy.number, copy.color, copy.fur_color, copy.graph, copy.finish_time, copy.name, copy.decal_image)
            #print(horse.print_items())

            horse.body.x = SCREEN_X - 17 * SIZE_FACTOR
            horse.body.y = round(self.body.y + i * 82 * SIZE_FACTOR)

            #pygame.draw.rect(screen, RED, horse.body)
            
            font = pygame.font.SysFont('Verdana', 6 * SIZE_FACTOR)
            
            text_surface = font.render(f"{horse.name} - {horse.odds[0]}:1 - {horse.finish_time}s", True, (255, 255, 255))

            text_rect = text_surface.get_rect()

        
            screen.blit(horse.fur_color[0], ((horse.body.x - 120 * SIZE_FACTOR), horse.body.y))
            screen.blit(horse.clothing_color_image, ((horse.body.x - 62 * SIZE_FACTOR), horse.body.y + 18 * SIZE_FACTOR))
            screen.blit(horse.decal_image, ((horse.body.x - 62 * SIZE_FACTOR), horse.body.y +  18 * SIZE_FACTOR))
            screen.blit(horse.number_image, ((horse.body.x - 63 * SIZE_FACTOR), horse.body.y + 16 * SIZE_FACTOR))

            screen.blit(text_surface, (horse.body.x - SIZE_FACTOR*115 + (SIZE_FACTOR*130 - text_rect.width)//2, horse.body.y + 80 * SIZE_FACTOR - 18 * SIZE_FACTOR, 0, 0))

    
        
class GraphicsHandler:
    def __init__(self, actionHandler, leaderboard, finish_line, podium):
        self.actionHandler = actionHandler
        self.leaderboard = leaderboard
        self.finish_line = finish_line
        self.podium = podium
        self.time = 0
        self.state = "menu"
        self.background = pygame.Rect(0, 0, SCREEN_X * 2, SCREEN_Y)
    

    def draw_horse(self, i):
        movement_bobble = 0
        horse = self.actionHandler.horses[i]
        
        if self.state == "menu":
            horse = self.actionHandler.numbered_horses[i]

            horse.body.x = (SCREEN_X - 600 * SIZE_FACTOR) // 2 + (120*SIZE_FACTOR) + i%4 * SIZE_FACTOR * 150
            horse.body.y = SCREEN_Y // 2 - SIZE_FACTOR * 75 if i < 4 else SCREEN_Y // 2 + SIZE_FACTOR * 75
            
            font = pygame.font.SysFont('Verdana', 8 * SIZE_FACTOR)
            
            text_surface = font.render(f"{horse.name} - {horse.odds[0]}:1", True, (0, 0, 0))

            text_rect = text_surface.get_rect()

            screen.blit(text_surface, (horse.body.x - SIZE_FACTOR*115 + (SIZE_FACTOR*130 - text_rect.width)//2, horse.body.y - 10 * SIZE_FACTOR, 0, 0))
        
            screen.blit(horse.fur_color[0], ((horse.body.x - 120 * SIZE_FACTOR), horse.body.y))
                

            

        elif self.state == "race":
            

            horse.move(self.time)

            horse.body.y = 40*SIZE_FACTOR + (i+1) * 24 * SIZE_FACTOR 
            #pygame.draw.rect(screen, RED, horse.body)
            
            screen.blit(horse.fur_color[self.time%9], ((horse.body.x - 120 * SIZE_FACTOR), horse.body.y))
            
            movement_bobble = self.time%9 / SIZE_FACTOR
        

        elif self.state == "freeze":
            horse.body.y = 40*SIZE_FACTOR + (i+1) * 24 * SIZE_FACTOR 
            #pygame.draw.rect(screen, RED, horse.body)
            
            screen.blit(horse.fur_color[self.time%9], ((horse.body.x - 120 * SIZE_FACTOR), horse.body.y))


        screen.blit(horse.clothing_color_image, ((horse.body.x - 62 * SIZE_FACTOR), horse.body.y + movement_bobble + 18 * SIZE_FACTOR))
        screen.blit(horse.decal_image, ((horse.body.x - 62 * SIZE_FACTOR), horse.body.y + movement_bobble + 18 * SIZE_FACTOR))
        screen.blit(horse.number_image, ((horse.body.x - 63 * SIZE_FACTOR), horse.body.y + movement_bobble + 16 * SIZE_FACTOR))

    def draw_horses(self):
        for i in range(8):
            self.draw_horse(i)
            

    def draw_leaderboard(self):

        self.leaderboard.adjust_ranking()

        for i in range(8):
            horse = self.leaderboard.ranking[i]
            surf = pygame.Surface((40*SIZE_FACTOR, 40*SIZE_FACTOR))

            surf.blit(pygame.transform.scale(horse.clothing_color_image, (27* 8* SIZE_FACTOR, 16 * 8 * SIZE_FACTOR)), (0, 0), (16 * SIZE_FACTOR, 17 * SIZE_FACTOR, 40*SIZE_FACTOR, 40*SIZE_FACTOR))
            #surf.blit(pygame.transform.scale(horse.decal_image, (27*4* SIZE_FACTOR, 16 * 4*SIZE_FACTOR)), (0, 0), (0, 0, 40*SIZE_FACTOR, 40*SIZE_FACTOR))

            outline_font = pygame.font.SysFont('Impact', 22 * SIZE_FACTOR)
            inline_font = pygame.font.SysFont('Impact', 18 * SIZE_FACTOR)
            font = pygame.font.SysFont('Impact', 20 * SIZE_FACTOR)
            
            outline_text_surface = outline_font.render(str(horse.number), True, (0, 0, 0))
            inline_text_surface = inline_font.render(str(horse.number), True, (0, 0, 0))
            text_surface = font.render(str(horse.number), True, (255, 255, 255))

            outline_text_rect = outline_text_surface.get_rect(center=(40*SIZE_FACTOR//2, 40*SIZE_FACTOR//2))
            inline_text_rect = inline_text_surface.get_rect(center=(40*SIZE_FACTOR//2, 40*SIZE_FACTOR//2))
            text_rect = text_surface.get_rect(center=(40*SIZE_FACTOR//2, 40*SIZE_FACTOR//2))

            surf.blit(outline_text_surface, outline_text_rect)
            surf.blit(inline_text_surface, inline_text_rect)
            surf.blit(text_surface, text_rect)
            screen.blit(surf, (SCREEN_X // 2 - 160*SIZE_FACTOR + 40*SIZE_FACTOR * i, 0))

    def move_background(self):
        if self.background.x > -(SCREEN_X - SCREEN_X // 60):
            self.background.x -= SCREEN_X // 30
        else:
            self.background.x = 0

    def draw_background(self):
        screen.blit(BACKGROUND, self.background)
        
    
    def draw_finish_line(self):
        pygame.draw.rect(screen, WHITE, self.finish_line.body)
        if self.finish_line.image_hidden == False:
            screen.blit(FINISH_LINE, (self.finish_line.body.x - FINISH_LINE.get_width() // 2 + SIZE_FACTOR, self.finish_line.body.y - FINISH_LINE.get_height()))

    def race(self):
        self.draw_background()
        self.move_background()

        self.finish_line.move(self.time)
        self.draw_finish_line()
        
        

        self.draw_horses()

        self.draw_leaderboard()
        
        if self.time < self.actionHandler.end_time:
            self.time += 1
        else:
            self.freeze_race()
    
    def draw_podium(self):
        screen.blit(PODIUM, self.podium.body)

    def freeze(self):
        self.draw_background()
        self.draw_finish_line()
        self.draw_horses()
        time.sleep(2)
        self.draw_podium()
        self.podium.horse_podium()
        # play photo sound and cheering
        #self.draw_leaderboard()

    def menu(self):
        self.draw_horses()

    def reset_race_state(self):
        self.time = 0
        # add things for resetting dynamic sprites such as stables

    def start_race(self):
        actionHandler.reset_horse_positions()
        self.reset_race_state()
        self.leaderboard = Leaderboard(self.actionHandler)
        self.finish_line = FinishLine(self.actionHandler)
        self.podium = Podium(self.actionHandler)
        self.state = "race"

    def freeze_race(self):
        self.state = "freeze"


    def handle_input(self, event):
        if event.key == pygame.K_SPACE:
            self.start_race()
            
        elif event.key == pygame.K_r:
            self.state = "menu"
            actionHandler.new_winner()
        elif event.key == pygame.K_n:
            self.state = "menu"
            actionHandler.generate_new_horses()

    def main(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    self.handle_input(event)
                    

            screen.fill(WHITE)

            if self.state == "race":
                self.race()
            elif self.state == "freeze":
                self.freeze()
            elif self.state == "menu":
                self.menu()

            pygame.display.update()
            
            clock.tick(10)






chanceHandler = ChanceHandler()
actionHandler = ActionHandler(chanceHandler)
actionHandler.generate_new_horses()

leaderboard = Leaderboard(actionHandler)
finish_line = FinishLine(actionHandler)
podium = Podium(actionHandler)
graphicsHandler = GraphicsHandler(actionHandler, leaderboard, finish_line, podium)


#chanceHandler.generate_odds()
graphicsHandler.main()

