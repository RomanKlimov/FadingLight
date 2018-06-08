import pygame

from entities.object import Object


class LightMath:
    @staticmethod
    def check_crossing(d11, d12, d21, d22, height=0):
        if height == 0:
            inv = 1
        else:
            inv = -1

        ab = pygame.math.Vector2(d22[0] - d21[0], (d22[1] * inv + height) - (d21[1] * inv + height))
        ac = pygame.math.Vector2(d11[0] - d21[0], (d11[1] * inv + height) - (d21[1] * inv + height))
        ad = pygame.math.Vector2(d12[0] - d21[0], (d12[1] * inv + height) - (d21[1] * inv + height))

        dc = pygame.math.Vector2(d11[0] - d12[0], (d11[1] * inv + height) - (d12[1] * inv + height))
        da = pygame.math.Vector2(d21[0] - d12[0], (d21[1] * inv + height) - (d12[1] * inv + height))
        db = pygame.math.Vector2(d22[0] - d12[0], (d22[1] * inv + height) - (d12[1] * inv + height))

        if dc.cross(da) * dc.cross(db) < 0 and ab.cross(ac) * ab.cross(ad) < 0:
            return True
        else:
            return False

    @staticmethod
    def get_cross_point(d11, d12, d21, d22, height=0):
        if height == 0:
            inv = 1
        else:
            inv = -1
        z1 = pygame.math.Vector2(d22[0] - d21[0], (d22[1] * inv + height) - (d21[1] * inv + height)).cross(
            pygame.math.Vector2(d11[0] - d21[0], (d11[1] * inv + height) - (
                d21[1] * inv + height)))
        z2 = pygame.math.Vector2(d22[0] - d21[0], (d22[1] * inv + height) - (d21[1] * inv + height)).cross(
            pygame.math.Vector2(d12[0] - d21[0], (
                d12[1] * inv + height) - (d21[1] * inv + height)))

        px = d11[0] + (d12[0] - d11[0]) * abs(z1) / abs(z2 - z1)
        py = d11[1] * inv + height + (d12[1] * inv + height - (d11[1] * inv + height)) * abs(z1) / abs(z2 - z1)
        return [px, height - py]

    @staticmethod
    def make_beams(object_list, light_source, height, n_factor=6, stupid_alg=True):
        def for_points_sort_by_angle(p):
            return pygame.math.Vector2(p[0] - light_source[0], p[1] - light_source[1]).angle_to(
                pygame.math.Vector2(0, 1))

        def for_lines_sort_by_angle(input_line):
            return pygame.math.Vector2(input_line[0][0] - light_source[0], input_line[0][1] - light_source[1]).angle_to(
                pygame.math.Vector2(0, 1))

        if not stupid_alg:
            lines_list = []
            for obj in object_list:
                for i in range(len(obj.point_list) - 1):
                    lines_list.append((obj.point_list[i], obj.point_list[i + 1]))
                lines_list.append((obj.point_list[len(obj.point_list) - 1], obj.point_list[0]))
            lines_list.sort(key=for_lines_sort_by_angle)

            separated_lines_lists = {n_factor: []}
            help_v1 = pygame.math.Vector2(0, 1)
            help_v2 = pygame.math.Vector2(0, 1).rotate(-360 / n_factor)

            for i in range(n_factor):
                separated_lines_lists[i] = []
                for line in lines_list:
                    q = False
                    if pygame.math.Vector2(line[0][0] - light_source[0],
                                           line[0][1] - light_source[1]).angle_to(help_v1) < 0:
                        if pygame.math.Vector2(line[0][0] - light_source[0],
                                               line[0][1] - light_source[1]).angle_to(help_v2) > 0:
                            if pygame.math.Vector2(line[1][0] - light_source[0],
                                                   line[1][1] - light_source[1]).angle_to(help_v1) < 0:
                                if pygame.math.Vector2(line[1][0] - light_source[0],
                                                       line[1][1] - light_source[1]).angle_to(help_v2) > 0:
                                    separated_lines_lists[i].append(line)
                                    q = True
                    if not q:
                        separated_lines_lists[n_factor].append(line)
                    lines_list.remove(line)
                help_v1.rotate(-360 / n_factor)
                help_v2.rotate(-360 / n_factor)

            rotate_factor = 0.00001
            final_point_list = []

            for obj in object_list:
                for obj_point in obj.point_list:
                    for q in range(2):
                        rotate_factor *= -1
                        min_cross = [9999, obj_point]
                        v = pygame.math.Vector2(obj_point[0] - light_source[0], obj_point[1] - light_source[1])
                        v1 = v.rotate(rotate_factor)
                        v1.x = v1.x * 1000
                        v1.y = v1.y * 1000
                        point = [0, 0]
                        point[0] = v1.x + light_source[0]
                        point[1] = v1.y + light_source[1]

                        help_v1 = pygame.math.Vector2(0, 1)
                        help_v2 = pygame.math.Vector2(0, 1).rotate(-360 / n_factor)

                        find_area = False
                        j = 0
                        while (not find_area) and (j < n_factor):
                            vec = pygame.math.Vector2(point[0] - light_source[0], point[1] - light_source[1])
                            if vec.cross(help_v1) > 0 and vec.cross(help_v2) > 0:
                                find_area = True
                            else:
                                j += 1
                                help_v1.rotate(-360 / n_factor)
                                help_v2.rotate(-360 / n_factor)
                        for line in separated_lines_lists[j]:
                            if LightMath.check_crossing(light_source, point, line[0], line[1],
                                                        height):
                                cross_pos = LightMath.get_cross_point(light_source, point, line[0], line[1], height)
                                if min_cross[0] > pygame.math.Vector2(light_source[0] - cross_pos[0],
                                                                      light_source[1] - cross_pos[1]).length():
                                    min_cross = [
                                        pygame.math.Vector2(light_source[0] - cross_pos[0],
                                                            light_source[1] - cross_pos[1]).length(),
                                        cross_pos]
                        for line in separated_lines_lists[n_factor]:
                            if LightMath.check_crossing(light_source, point, line[0], line[1],
                                                        height):
                                cross_pos = LightMath.get_cross_point(light_source, point, line[0], line[1], height)
                                if min_cross[0] > pygame.math.Vector2(light_source[0] - cross_pos[0],
                                                                      light_source[1] - cross_pos[1]).length():
                                    min_cross = [
                                        pygame.math.Vector2(light_source[0] - cross_pos[0],
                                                            light_source[1] - cross_pos[1]).length(),
                                        cross_pos]
                        final_point_list.append(min_cross[1])
            final_point_list.sort(key=for_points_sort_by_angle)
            # print(separated_lines_lists)
            return final_point_list
        # ----------------------------------------------------------------
        else:
            r_f = 0.00001
            array = []
            for obj in object_list:
                for obj_point in obj.point_list:
                    for w in range(2):
                        r_f *= -1
                        cross_pos = [-1, -1]
                        min_cross = [9999, obj_point]
                        v = pygame.math.Vector2(obj_point[0] - light_source[0], obj_point[1] - light_source[1])
                        v1 = v.rotate(r_f)
                        v1.x = v1.x * 1000
                        v1.y = v1.y * 1000
                        point = [0, 0]
                        point[0] = v1.x + light_source[0]
                        point[1] = v1.y + light_source[1]

                        for obj1 in object_list:
                            for i in range(len(obj1.point_list) - 1):
                                if LightMath.check_crossing(light_source, point, obj1.point_list[i],
                                                            obj1.point_list[i + 1],
                                                            height):
                                    cross_pos = LightMath.get_cross_point(light_source, point, obj1.point_list[i],
                                                                          obj1.point_list[i + 1], height)
                                    if min_cross[0] > pygame.math.Vector2(light_source[0] - cross_pos[0],
                                                                          light_source[1] - cross_pos[1]).length():
                                        min_cross = [
                                            pygame.math.Vector2(light_source[0] - cross_pos[0],
                                                                light_source[1] - cross_pos[1]).length(),
                                            cross_pos]
                            if LightMath.check_crossing(light_source, point, obj1.point_list[len(obj1.point_list) - 1],
                                                        obj1.point_list[0], height):
                                cross_pos = LightMath.get_cross_point(light_source, point,
                                                                      obj1.point_list[len(obj1.point_list) - 1],
                                                                      obj1.point_list[0], height)
                                if min_cross[0] > pygame.math.Vector2(light_source[0] - cross_pos[0],
                                                                      light_source[1] - cross_pos[1]).length():
                                    min_cross = [pygame.math.Vector2(light_source[0] - cross_pos[0],
                                                                     light_source[1] - cross_pos[1]).length(),
                                                 cross_pos]
                        array.append(min_cross[1])

            array.sort(key=for_points_sort_by_angle)
            return array

    @staticmethod
    def make_beams_reduced(object_list, light_source, height, width):
        def spec_sort(p):
            def for_points_sort_by_angle(p1):
                return pygame.math.Vector2(p1[0] - spec_pos[0], p1[1] - spec_pos[1]).angle_to(
                    pygame.math.Vector2(1, 0))
            return for_points_sort_by_angle(p)

        walls = Object([[0, 0], [width, 0], [width, height], [0, height]])
        r_f = 0.00001
        array = []
        for obj in object_list:
            part_array = []
            for obj_point in obj.point_list:
                for w in range(2):
                    r_f *= -1
                    cross_pos = [-1, -1]
                    min_cross = [9999, obj_point]
                    v = pygame.math.Vector2(obj_point[0] - light_source[0], obj_point[1] - light_source[1])
                    v1 = v.rotate(r_f)
                    v1.x = v1.x * 1000
                    v1.y = v1.y * 1000
                    point = [0, 0]
                    point[0] = v1.x + light_source[0]
                    point[1] = v1.y + light_source[1]

                    for i in range(len(obj.point_list) - 1):
                        if LightMath.check_crossing(light_source, point, obj.point_list[i], obj.point_list[i + 1],
                                                    height):
                            cross_pos = LightMath.get_cross_point(light_source, point, obj.point_list[i],
                                                                  obj.point_list[i + 1], height)
                            if min_cross[0] > pygame.math.Vector2(light_source[0] - cross_pos[0],
                                                                  light_source[1] - cross_pos[1]).length():
                                min_cross = [
                                    pygame.math.Vector2(light_source[0] - cross_pos[0],
                                                        light_source[1] - cross_pos[1]).length(),
                                    cross_pos]
                        if LightMath.check_crossing(light_source, point, obj.point_list[len(obj.point_list) - 1],
                                                    obj.point_list[0], height):
                            cross_pos = LightMath.get_cross_point(light_source, point,
                                                                  obj.point_list[len(obj.point_list) - 1],
                                                                  obj.point_list[0], height)
                            if min_cross[0] > pygame.math.Vector2(light_source[0] - cross_pos[0],
                                                                  light_source[1] - cross_pos[1]).length():
                                min_cross = [pygame.math.Vector2(light_source[0] - cross_pos[0],
                                                                 light_source[1] - cross_pos[1]).length(), cross_pos]
                    for i in range(len(walls.point_list) - 1):
                        if LightMath.check_crossing(light_source, point, walls.point_list[i], walls.point_list[i + 1],
                                                    height):
                            cross_pos = LightMath.get_cross_point(light_source, point, walls.point_list[i],
                                                                  walls.point_list[i + 1], height)
                            if min_cross[0] > pygame.math.Vector2(light_source[0] - cross_pos[0],
                                                                  light_source[1] - cross_pos[1]).length():
                                min_cross = [
                                    pygame.math.Vector2(light_source[0] - cross_pos[0],
                                                        light_source[1] - cross_pos[1]).length(),
                                    cross_pos]
                    if LightMath.check_crossing(light_source, point, walls.point_list[len(walls.point_list) - 1],
                                                walls.point_list[0], height):
                        cross_pos = LightMath.get_cross_point(light_source, point,
                                                              walls.point_list[len(walls.point_list) - 1],
                                                              walls.point_list[0], height)
                        if min_cross[0] > pygame.math.Vector2(light_source[0] - cross_pos[0],
                                                              light_source[1] - cross_pos[1]).length():
                            min_cross = [pygame.math.Vector2(light_source[0] - cross_pos[0],
                                                             light_source[1] - cross_pos[1]).length(), cross_pos]
                    part_array.append(min_cross[1])
            spec_point_x0 = []
            spec_point_x1 = []
            spec_point_y0 = []
            spec_point_y1 = []
            med_x = 0
            med_y = 0
            for point in part_array:
                med_x += point[0]
                med_y += point[1]
                if -0.1 < point[0] < 0.1:
                    spec_point_x0.append(point)
                if width - 0.1 < point[0] < width + 0.1:
                    spec_point_x1.append(point)
                if -0.1 < point[1] < 0.1:
                    spec_point_y0.append(point)
                if height - 0.1 < point[1] < height + 0.1:
                    spec_point_y1.append(point)
            med_y = med_y / len(part_array)
            med_x = med_x / len(part_array)
            if len(spec_point_x0) != 0 and len(spec_point_y0) != 0:
                part_array = [[0, 0]] + part_array
            if len(spec_point_x1) != 0 and len(spec_point_y1) != 0:
                part_array += [[width, height]]
            if len(spec_point_x0) != 0 and len(spec_point_y1) != 0:
                part_array += [[0, height]]
            if len(spec_point_x1) != 0 and len(spec_point_y0) != 0:
                part_array += [[width, 0]]
            if len(spec_point_x1) != 0 and len(spec_point_x0) != 0 and med_y > light_source[1]:
                part_array += [[0, height], [width, height]]
            if len(spec_point_x1) != 0 and len(spec_point_x0) != 0 and med_y < light_source[1]:
                part_array += [[0, 0], [width, 0]]
            if len(spec_point_y1) != 0 and len(spec_point_y0) != 0 and med_x > light_source[0]:
                part_array += [[width, 0], [width, height]]
            if len(spec_point_y1) != 0 and len(spec_point_y0) != 0 and med_x < light_source[0]:
                part_array += [[0, 0], [0, height]]
            spec_pos = (med_x, med_y)
            part_array.sort(key=spec_sort)
            array.append(Object(part_array, obj.shadow_type))
            # array.append(part_array)

        return array

