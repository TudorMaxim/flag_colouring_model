LOADING_SPINNER_ANIMATION = './assets/loading_spinner.gif'
DEFAULT_DATASET = './datasets/dataset_c8_s12_t3.json'
POPULATION_CNT = 100
GENERATIONS_CNT = 100
MUTATION_PROBABILITY = 60
COLOURS_CNT = 60
MAX_COURSES_PER_DAY = 6
MAX_DAILY_BREAK = 2 # hours
IVALID_COLOURING_PENALTY = 2 ** 10 # applied if a colour is invalid
OVERCROWDING_PENALTY = 2 ** 6 # applied if a student/teacher has more than 6 courses a day
FRAGMENTATION_PENALTY = 2 ** 5 # applied for each break longer than 2 hours for a teacher
UNIFORMITY_PENALTY = 2 ** 4 # multiplied with the difference between the longest and shortest day of a teacher
COLORS = ['',
    '#1E90FF', '#D71868', '#50C878', '#6F00FF', '#CCFF00', '#BF00FF', '#8F00FF', '#B53389', '#B22222', '#E25822',
    '#B0BF1A', '#7CB9E8', '#C0E8D5', '#B284BE', '#72A0C1', '#EDEAE0', '#C46210', '#EFDECD', '#3B7A57', '#FFBF00',
    '#FF7E00', '#9966CC', '#3DDC84', '#CD9575', '#665D1E', '#915C83', '#841B2D', '#FAEBD7', '#8DB600', '#00FFFF',
    '#7FFFD4', '#8F9779', '#007FFF', '#89CFF0', '#F4C2C2', '#DA1884', '#9C2542', '#967117', '#FE6F5E', '#3D0C02',
    '#318CE7', '#7366BD', '#126180', '#064E40', '#A2A2D0', '#006A4E', '#87413F', '#CB4154', '#D891EF', '#004225',
    '#A67B5B', '#960018', '#703642', '#007AA5', '#7B3F00', '#5D3954', '#536878', '#1A2421', '#00CED1', '#EDC9AF'
]
