import bpy
def find_area():
    try:
        for a in bpy.data.window_managers[0].windows[0].screen.areas:
            if a.type == "VIEW_3D":
                return a
        return None
    except:
        return None

area = find_area()

if area is None:
    print("area not find")
else:
    # print(dir(area))
    r3d = area.spaces[0].region_3d
    view_mat = r3d.view_matrix
    print("view matrix: ", view_mat)

    loc, rot, sca = view_mat.decompose()
    print("location xyz: ", loc)
    print("rotation wxyz: ", rot)
    print("scale xyz: ", sca)
    print("")
    print("view_distance: ", r3d.view_distance)
    print("view_location: ", r3d.view_location)
    print("view_rotation: ", r3d.view_rotation)
    print("view_camera_zoom: ", r3d.view_camera_zoom)
    print("view_distance: ", r3d.view_distance)
    print("view_camera_offset: ", r3d.view_camera_offset)


# ['__doc__', '__module__', '__slots__', 'bl_rna', 'clip_planes', 'is_orthographic_side_view', 'is_perspective', 'lock_rotation', 'perspective_matrix', 'rna_type', 'show_sync_view', 'update', 'use_box_clip', 'use_clip_planes', 'view_camera_offset', 'view_camera_zoom', 'view_distance', 'view_location', 'view_matrix', 'view_perspective', 'view_rotation', 'window_matrix']
