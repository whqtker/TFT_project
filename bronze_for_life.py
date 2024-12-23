from db import get_data, insert_data

def count_all_traits(selected_champions, set):
    champions_data = get_data('tft', 'champions')

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

    return trait_count

# set 시즌의 trait_count에서 활성화된 특성 리턴
def count_active_traits(trait_count, set):
    traits_data = get_data('tft', 'traits')
    
    active_traits = {}
    
    # 카운트된 traits를 기반으로 active traits를 결정
    for trait, count in trait_count.items():
        styles = next((t['styles'] for t in traits_data if t['key'] == trait), [])
        for style in styles:
            if style['min'] <= count <= style.get('max', float('inf')):
                active_traits[trait] = style['style']
                break
    
    return active_traits

# set_number 시즌 챔피언 중 1~level 크기의 모든 팀 조합 생성
def generate_possible_combinations(level, set_number):
    champions_data = get_data('tft', 'champions')
    champions_data = [champion for champion in champions_data if champion['set'] == "set" + str(set_number)]
    
    champions = {champion['name']: champion['traits'] for champion in champions_data}
    
    def backtrack(current_team, remaining_slots):
        if remaining_slots == 0:
            trait_count = count_all_traits(current_team, set_number)
            insert_data('tft', 'combinations', {
                'team': current_team,
                'traits': trait_count,
                'team_size': len(current_team),
                'set_number': set_number
            })
            return
        
        for champion in champions.items():
            if champion in current_team:
                continue
            new_team = current_team + [champion]
            backtrack(new_team, remaining_slots - 1)
    
    for team_size in range(1, level + 1):
        backtrack([], team_size)

level = 13 # 배치 가능한 챔피언 수
set_number = 13 # 시즌 번호

generate_possible_combinations(level, set_number)