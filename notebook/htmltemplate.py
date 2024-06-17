##### HTML variables and html strings used in shp2html.ipynb

HTMLHEAD = '<!DOCTYPE html>\n<html>\n<head>\n\t<title>Image Map</title>\n'\
    '\t<meta charset="utf-8">\n\t<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>\n'\
    '\t<script src="https://cdnjs.cloudflare.com/ajax/libs/image-map-resizer/1.0.10/js/imageMapResizer.min.js"></script>\n'\
        '</head>\n<body>\n'   
HTMLFOOT = '<script>\n\t$(document).ready(function() {\n\t $(\'map\').imageMapResize();\n\t}); \n</script>\n</body>\n</html>'    

##### KMZ2HTML variables and html strings used in kmz2html.ipynb

#1. HTML header
#TODO: change name using variables or arguments
KMZ_HTMLHEAD = '<!DOCTYPE html>\n<html>\n<head>\n\t<title>KML 3D web Viewer</title>\n</head>\n<body>'

# ----  HTML body -----
#2. Importing Javascript libraries from CDN servers
#TODO: Add a list of CDN servers for the libraries in the future
# for example: CDN_SERVERS = ['https://cdn.jsdelivr.net/npm/three@0.151.3/build/three.module.js', 'https://unpkg.com/']
KMZ_IMPORTLIBS= '<script type="importmap"> \n'\
    '\t {"imports": \n'\
        '\t{\n'\
            '\t "three": "https://unpkg.com/three/build/three.module.js",\n'\
            '\t "three/addons/": "./three/addons/jsm/"\n'\
        '\t} \n'\
    '} \n'\
    '</script>\n'
#Save threeJS addons file inside folder of project
def KMZ_THREEJS_ADDONS_FILES_ADD_TO_PROJECT(projectName):
    import os
    import shutil
    # create folder for project if does not exist
    if not os.path.exists(projectName):
        os.makedirs(projectName)
    # create Three folder for addons if does not exist
    if not os.path.exists(projectName + '/three'):
        os.makedirs(projectName + '/three')
    # create addon folder for addons if does not exist
    if not os.path.exists(projectName + '/three/addons'):
        os.makedirs(projectName + '/three/addons')
    # create jsm folder for addons if does not exist
    if not os.path.exists(projectName + '/three/addons/jsm'):
        os.makedirs(projectName + '/three/addons/jsm')
    # create subfolders of controls if does not exist
    if not os.path.exists(projectName + '/three/addons/jsm/controls'):
        os.makedirs(projectName + '/three/addons/jsm/controls')
    if not os.path.exists(projectName + '/three/addons/jsm/loaders'):
        os.makedirs(projectName + '/three/addons/jsm/loaders')
    if not os.path.exists(projectName + '/three/addons/jsm/libs'):
        os.makedirs(projectName + '/three/addons/jsm/libs')
    # copy the files to the project folder
    # OrbitControls.js
    if not os.path.exists(projectName + '/three/addons/jsm/controls/OrbitControls.js'):
        shutil.copy('three/addons/jsm/controls/OrbitControls.js', projectName + '/three/addons/jsm/controls/')
    # fflate.module.js
    if not os.path.exists(projectName + '/three/addons/jsm/libs/fflate.module.js'):
        shutil.copy('three/addons/jsm/libs/fflate.module.js', projectName + '/three/addons/jsm/libs/')
    # ColladaLoader.js
    if not os.path.exists(projectName + '/three/addons/jsm/loaders/ColladaLoader.js'):
        shutil.copy('three/addons/jsm/loaders/ColladaLoader.js', projectName + '/three/addons/jsm/loaders/')
    # KMZLoader.js
    if not os.path.exists(projectName + '/three/addons/jsm/loaders/KMZLoader.js'):
        shutil.copy('three/addons/jsm/loaders/KMZLoader.js', projectName + '/three/addons/jsm/loaders/')
    # TGALoader.js
    if not os.path.exists(projectName + '/three/addons/jsm/loaders/TGALoader.js'):
        shutil.copy('three/addons/jsm/loaders/TGALoader.js', projectName + '/three/addons/jsm/loaders/')    
    return 


#3. Opening script tag
KMZ_OPENINGSCRIPT = '<script type="module">\n'

#4. Javascript code to load an GIFimage as a splash screen
def KMZ_LOADINGIMAGE(SPLASHIMAGE_URI):
    HTMLstring = '	// Loading image\n'\
	'\t var loadingImage = document.createElement(\'img\');\n'\
	'\t loadingImage.src = \'' + SPLASHIMAGE_URI + '\';   \n'\
	'\t loadingImage.id = \'loadingImage\';   \n'\
	'\t loadingImage.style.position = \'fixed\';  \n'\
	'\t loadingImage.style.top = \'0\';   \n'\
	'\t loadingImage.style.left = \'0\';  \n'\
	'\t loadingImage.style.width = \'100vw\'; \n'\
	'\t loadingImage.style.height = \'100vh\';    \n'\
	'\t loadingImage.style.objectFit = \'cover\'; \n'\
	'\t loadingImage.style.zIndex = \'9999\'; \n'\
	'\t document.body.appendChild(loadingImage);    \n'\
	'\t setTimeout(function(){                          \n'\
	'\t 	// Remove loading image after 10 seconds \n'\
	'\t 	var loadingImage = document.getElementById(\'loadingImage\'); \n'\
    '\t 	loadingImage.parentNode.removeChild(loadingImage); \n'\
	'\t 	}, 3000); \n'\
	'\t \n'
    return HTMLstring

# Javascript code to load the KMZ file
#5. Open main Three.JS script
def KMZ_THREEJS_script(KMZ_URI):
    HTML_string = '	// Three.js script                              \n'\
        '\t import * as THREE from \'three\';                       \n'\
        '\t import { OrbitControls } from \'three/addons/controls/OrbitControls.js\';        \n'\
        '\t 	import { KMZLoader } from \'three/addons/loaders/KMZLoader.js\';            \n'\
        '\t 		let camera, scene, renderer;                    \n'\
        '\t 		init();                                         \n'\
        '\t function init() {                                       \n'\
		'\t 		scene = new THREE.Scene();                      \n'\
		'\t 		scene.background = new THREE.Color( 0x999999 );             \n'\
		'\t 		const light = new THREE.DirectionalLight(0xffffff, 1);      \n'\
		'\t 		// light.position.set( 1, 10, 1 ).normalize();              \n'\
		'\t 		light.position.set( 1, 10, 1 );                             \n'\
		'\t 		scene.add( light );                                         \n'\
		'\t 		camera = new THREE.PerspectiveCamera( 35, window.innerWidth / window.innerHeight, 1, 500 );\n'\
		'\t 		camera.position.y = 30;                                     \n'\
		'\t 		camera.position.z = 100;                                    \n'\
		'\t 		scene.add( camera );                                        \n'\
		'\t 		const grid = new THREE.GridHelper( 50, 50, 0xffffff, 0x7b7b7b );\n'\
		'\t 		scene.add( grid );                                          \n'\
		'\t 		renderer = new THREE.WebGLRenderer( { antialias: true } );  \n'\
		'\t 		renderer.setPixelRatio( window.devicePixelRatio );          \n'\
		'\t 		renderer.setSize( window.innerWidth, window.innerHeight );  \n'\
		'\t 		document.body.appendChild( renderer.domElement );           \n'\
		'\t 		const loader = new KMZLoader();                             \n'\
		'\t 		loader.load( \'' + KMZ_URI + '\', function ( kmz ) {        \n'\
		'\t 			kmz.scene.position.y = -40; // NOTE: y is the vertical axis \n'\
		'\t 			scene.add( kmz.scene );                                 \n'\
		'\t 			render();                                               \n'\
		'\t 		// Arrow Geometry                                           \n'\
		'\t 		// step 1 add box                                           \n'\
		'\t 		var geometry = new THREE.BoxGeometry(0.5, 0.5, 10);         \n'\
		'\t 		var material = new THREE.MeshBasicMaterial({color: 0x8B0000});\n'\
		'\t 		var cube = new THREE.Mesh(geometry, material);              \n'\
		'\t 		cube.position.set(10,10,10)                                 \n'\
		'\t 		scene.add(cube);                                            \n'\
		'\t 		// step 2 add arrow                                         \n'\
		'\t 		var geometry2 = new THREE.CylinderGeometry( 1, 0.5, 0.5, 3 );\n'\
		'\t 		var material2 = new THREE.MeshBasicMaterial( {color: 0x8B0000} );\n'\
		'\t 		var prism = new THREE.Mesh( geometry2, material2 );         \n'\
		'\t 		prism.position.set(10,10,15)                                \n'\
		'\t 		scene.add( prism );                                         \n'\
		'\t 		} );                                                        \n'\
		'\t 		const controls = new OrbitControls( camera, renderer.domElement );\n'\
		'\t 		controls.addEventListener( \'change\', render );            \n'\
		'\t 		controls.update();                                          \n'\
		'\t 		window.addEventListener( \'resize\', onWindowResize );      \n'\
		'\t 	}                                                               \n'\
		'\t 	function onWindowResize() {                                     \n'\
		'\t 		camera.aspect = window.innerWidth / window.innerHeight;     \n'\
		'\t 		camera.updateProjectionMatrix();                            \n'\
		'\t 		renderer.setSize( window.innerWidth, window.innerHeight );  \n'\
		'\t 		render();                                                   \n'\
		'\t 	}                                                               \n'\
		'\t 	function render() {                                             \n'\
		'\t 		renderer.render( scene, camera );                           \n'\
		'\t 	}                                                               \n'
    return HTML_string
# close script tag
KMZ_CLOSINGSCRIPT = '</script>\n'

# style tag
KMZ_STYLE = '<style> body { margin: 0; } </style>'

# html footer and closing tags
KMZ_HTMLFOOT = '\n</body>\n</html>'