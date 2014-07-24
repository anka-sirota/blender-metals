import bpy

MATERIAL_NAME = 'steel'
ROUGH = True

MATERIAL_SETTINGS = {
    'gold': {
        'specular_color': (1, 0.798777, 0.345904),
        'specular_intensity': {
            True: 0.5,
            False: 0.8,
        },
        'specular_slope': 0.4,
        'specular_ramp': (
            (0.838181, 1, 0.308132, 0),
            (1, 0.551188, 0.188334, 1)
        ),
        'specular_ramp_factor': 0.4,
        'specular_ramp_input': 'SHADER',
        'diffuse_color': {
            True: (1, 0.798777, 0.345904),
            False: (0, 0, 0),
        },
        'diffuse_intensity': {
            True: 0.01,
            False: 0,
        },
        'diffuse_ramp': (
            (0.973445, 0.625763, 0.21453, 0),
            (0.835062, 1, 0.401978, 1),
        ),
        'mirror_color': (1, 0.895247, 0.353817),
        'reflect_factor': {
            True: 0.1,
            False: 0.9,
        },
        'fresnel': {
            True: 1,
            False: 2.5,
        },
        'gloss_factor': 1,
    },
    'bronze': {
        'specular_color': (1, 0.573, 0.239),
        'specular_intensity': {
            True: 0.2,
            False: 0.8,
        },
        'specular_slope': 0.2,
        'specular_ramp': (
            (0.838181, 1, 0.308132, 0),
            (1, 0.734506, 0.2057, 1)
        ),
        'specular_ramp_factor': 0.2,
        'specular_ramp_input': 'SHADER',
        'diffuse_color': {
            True: (0.022, 0.009, 0.006),
            False: (0.022, 0.009, 0.006),
        },
        'diffuse_intensity': {
            True: 0.05,
            False: 0.05,
        },
        'diffuse_ramp': (
            (0.130299, 0.0302682, 0.00446032, 0),
            (0.022, 0.009, 0.006, 1),
        ),
        'diffuse_ramp_factor': 0.2,
        'specular_slope': 0.1,
        'mirror_color': (1, 0.634, 0.274),
        'reflect_factor': {
            True: 0.3,
            False: 0.9,
        },
        'fresnel': {
            True: 1,
            False: 2.5,
        },
        'gloss_factor': 0.8,
    },
    'steel': {
        'specular_color': (1, 1, 1),
        'specular_intensity': {
            True: 0.15,
            False: 0.3,
        },
        'specular_slope': 0.1,
        'specular_ramp': (
            (0.571, 0.887, 1, 0),
            (1, 0.900, 0.575, 1)
        ),
        'specular_ramp_factor': 0.1,
        'specular_ramp_input': 'RESULT',
        'diffuse_color': {
            True: (0.01, 0.01, 0.01),
            False: (0, 0, 0),
        },
        'diffuse_intensity': {
            True: 0.05,
            False: 0,
        },
        'diffuse_ramp': (
            (0.003, 0.001, 0.0003, 1),
            (0.001, 0.003, 0.006, 0),
        ),
        'diffuse_ramp_factor': 0.2,
        'mirror_color': (1, 1, 1),
        'reflect_factor': {
            True: 0.3,
            False: 0.9,
        },
        'fresnel': {
            True: 1,
            False: 2.5,
        },
        'gloss_factor': 0.8,
    },
}


def init_metal(name, rough=False):
    obj = bpy.context.object
    texture_name = '{}_normal'.format(name)
    settings = MATERIAL_SETTINGS[name]

    material = bpy.data.materials.new('gold')

    # setting up diffuse
    material.diffuse_color = settings['diffuse_color'][rough]
    material.diffuse_intensity = settings['diffuse_intensity'][rough]
    material.use_diffuse_ramp = rough
    if material.use_diffuse_ramp:
        material.diffuse_ramp.elements[0].color, \
            material.diffuse_ramp.elements[1].color = settings['diffuse_ramp']
    material.use_mist = False

    # setting up mirror
    material.raytrace_mirror.use = True
    material.raytrace_mirror.gloss_factor = settings['gloss_factor']
    material.raytrace_mirror.gloss_threshold = 0.1
    material.raytrace_mirror.gloss_samples = 10
    material.raytrace_mirror.gloss_anisotropic = 0.9
    material.raytrace_mirror.fresnel = settings['fresnel'][rough]
    material.raytrace_mirror.fresnel_factor = 1.3
    material.raytrace_mirror.depth = 1
    material.raytrace_mirror.distance = 5
    material.raytrace_mirror.reflect_factor = settings['reflect_factor'][rough]
    material.mirror_color = settings['mirror_color']

    # setting up specular
    material.use_specular_ramp = True
    material.specular_ramp.interpolation = 'B_SPLINE'
    material.specular_hardness = 100
    material.specular_ramp.elements[0].color = settings['specular_ramp'][0]
    material.specular_ramp.elements[1].color = settings['specular_ramp'][1]
    material.specular_ramp_factor = settings['specular_ramp_factor']
    material.specular_ramp_input = settings['specular_ramp_input']
    material.specular_color = settings['specular_color']
    material.specular_shader = 'WARDISO'
    material.specular_intensity = settings['specular_intensity'][rough]
    material.specular_slope = settings['specular_slope']

    # prepare procedural texture for normals
    bpy.data.textures.new(texture_name, 'DISTORTED_NOISE')
    texture = bpy.data.textures[texture_name]
    texture.noise_distortion = 'VORONOI_F2_F1'
    texture.distortion = rough and 5 or 10
    texture.nabla = 0.1
    texture.noise_scale = 0.03

    # adding texture to the material
    material.texture_slots.add()
    material.texture_slots[0].texture = texture
    material.texture_slots[0].use_map_color_diffuse = False
    material.texture_slots[0].use_map_normal = True
    material.texture_slots[0].normal_factor = rough and 0.07 or 0.01
    material.texture_slots[0].mapping = 'CUBE'

    # assigning material
    obj.material_slots[0].material = material


def test_all():
    for name in MATERIAL_SETTINGS.keys():
        for rough in (True, False):
            bpy.data.scenes[0].render.filepath = './test_{}_{}.png'.format(
                name, rough and 'rough' or 'polished')
            init_metal(name, rough)
            bpy.ops.render.render(write_still=True)

#init_metal(MATERIAL_NAME, ROUGH)
test_all()
