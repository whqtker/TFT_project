from db import get_data
from itertools import combinations

# set 시즌의 selected_champions으로 구성된 팀의 활성화된 특성 리턴
def count_active_traits(selected_champions, set):
    champions_data = get_data('tft', 'champions')
    traits_data = get_data('tft', 'traits')

    # 선택된 세트에 해당하는 챔피언 데이터만 추출
    champions_data = [champion for champion in champions_data if champion['set'] == "set" + str(set)] 

    # 챔피언 이름을 key로, traits를 value로 하는 딕셔너리 생성
    champions = {champion['name']: champion['traits'] for champion in champions_data}
    
    trait_count = {}
    
    # 선택된 챔피언들의 traits를 카운트
    for champion in selected_champions:
        traits = champions.get(champion, [])
        for trait in traits:
            if trait in trait_count:
                trait_count[trait] += 1
            else:
                trait_count[trait] = 1
    
    active_traits = {}
    
    # 카운트된 traits를 기반으로 active traits를 결정
    for trait, count in trait_count.items():
        styles = next((t['styles'] for t in traits_data if t['key'] == trait), [])
        for style in styles:
            if style['min'] <= count <= style.get('max', float('inf')):
                active_traits[trait] = style['style']
                break
    
    return active_traits

def generate_possible_combinations(level, selected_champions, set):
    remaining_slots = level - len(selected_champions) # 배치 가능한 챔피언 수

    if remaining_slots <= 0:
        print("선택된 챔피언 수가 레벨보다 많습니다.")
        return []
    
    champions_data = get_data('tft', 'champions')
    champions_data = [champion for champion in champions_data if champion['set'] == "set" + str(set)]

    # 배치 가능한 챔피언 후보들
    remained_champions = [champion['name'] for champion in champions_data if champion['name'] not in selected_champions and champion['traits']]

    possible_combinations = []

    for index, combo in enumerate(combinations(remained_champions, remaining_slots)):
        print(f"Processing combination {index + 1}/{len(list(combinations(remained_champions, remaining_slots)))}")
        full_team = selected_champions + list(combo)
        active_traits = count_active_traits(full_team, set)
        possible_combinations.append((full_team, active_traits))
    
    return possible_combinations

def sort_and_print_combinations(possible_combinations):
    sorted_combinations = sorted(possible_combinations, key=lambda x: sum(1 for style in x[1].values() if style == 'bronze'), reverse=True)
    
    for team, traits in sorted_combinations[:10]:
        print(f"Team: {team}")
        print(f"Active Traits: {traits}")
        print(f"활성화된 브론즈 특성 수: {sum(1 for style in traits.values() if style == 'bronze')}")
        print()

level = 5
selected_champions = ["암베사", "말자하", "렐"]
set = 13

possible_combinations = generate_possible_combinations(level, selected_champions, set)
sort_and_print_combinations(possible_combinations)