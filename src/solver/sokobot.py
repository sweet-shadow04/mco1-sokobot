import time
import heapq
from collections import deque

class SokoBot:
    def precompute_distances(self, goals, walls):
        distances = {}
        queue = deque()
        
        for g in goals:
            distances[g] = 0
            queue.append(g)
            
        while queue:
            current_r, current_c = queue.popleft()
            current_dist = distances[(current_r, current_c)]
            
            neighbors = [
                (current_r - 1, current_c),
                (current_r + 1, current_c),
                (current_r, current_c - 1),
                (current_r, current_c + 1)
            ]
            
            for nr, nc in neighbors:
               if (nr, nc) not in walls and (nr, nc) not in distances:
                distances[(nr, nc)] = current_dist + 1
                queue.append((nr, nc))
                pass 
                
        return distances

    def computeHeuristic(self, crates, distances):
        total_distance = 0
        for c in crates:
            if c in distances:
                total_distance += distances[c]
            else:
                return float('inf') 
        return total_distance

    def isCornerDeadlock(self, crate_target, walls):
        crate_target = list(crate_target)
        up = (crate_target[0] - 1, crate_target[1]) in walls
        down = (crate_target[0] + 1, crate_target[1]) in walls
        left = (crate_target[0], crate_target[1] - 1) in walls
        right = (crate_target[0], crate_target[1] + 1) in walls
        
        if (up and left) or (up and right) or (down and left) or (down and right):
            return True

        return False

    def solveSokobanPuzzle(self, width, height, mapData, itemsData):
        walls = set()
        goals = set()
        player = None
        crates = set()

        for r in range(height):
            for c in range(width):
                if mapData[r][c] == '.':
                    goals.add((r, c))
                elif mapData[r][c] == '#':
                    walls.add((r, c))
        
        for r in range(height):
            for c in range(width):
                if itemsData[r][c] == '@':
                    player = (r, c)
                elif itemsData[r][c] == '$':
                    crates.add((r, c))

        # 1. Call the precomputation here
        distances = self.precompute_distances(goals, walls)

        start_state = (player, tuple(crates))
        frontier = []
        heapq.heapify(frontier)
        visited = set()

        # 2. Update initial heuristic call
        heuristic_start = self.computeHeuristic(list(crates), distances)
        heapq.heappush(frontier, (heuristic_start, start_state, ""))
        visited.add(start_state)

        moves = [('u', -1, 0), ('d', 1, 0), ('l', 0, -1), ('r', 0, 1)]

        while frontier:         
            h, cur_state, path = heapq.heappop(frontier)

            if set(cur_state[1]) >= goals:
                return path
            
            for dir_char, dx, dy in moves:
                next_player = (cur_state[0][0] + dx, cur_state[0][1] + dy)

                if next_player in walls:
                    continue

                next_crates = (set(cur_state[1])).copy()

                if next_player in cur_state[1]:
                    crate_target = (next_player[0] + dx, next_player[1] + dy)

                    if crate_target in walls or crate_target in cur_state[1]:
                        continue
                    if self.isCornerDeadlock(crate_target, walls) and crate_target not in goals:
                        continue
                        
                    next_crates.remove(next_player)
                    next_crates.add(crate_target)

                next_state = (next_player, tuple(next_crates))
                if next_state not in visited:
                    visited.add(next_state)
                    # 3. Update the loop's heuristic call
                    heuristicVal = self.computeHeuristic(list(next_crates), distances)
                    heapq.heappush(frontier, (heuristicVal, next_state, path + dir_char))
