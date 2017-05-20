var Fractal = function(numPoints, transformString) {
	var transformParts = transformString.split(/ /),
		numTransforms = transformParts.length / 16, 
		transforms = [],
		points = navigator.userAgent.toLowerCase().indexOf('firefox') > -1 
			? new Array(numPoints * 4) : [], //http://jsperf.com/pre-allocated-arrays
		i, j, rand, rint, t, x, y, z, w, start, 
		discard = true, discardCount = 500;//make this divisible by 4!
	
	for (i = 0; i < numTransforms; i++) {
		transforms[i] = [];
		for (j = 0; j < 16; j++) {
			transforms[i][j] = parseFloat(transformParts[i * 16 + j]);
		}
	}
	points[0] = Math.random() * 2 - 1;
	points[1] = Math.random() * 2 - 1;
	points[2] = Math.random() * 2 - 1;
	points[3] = 1;
	
	var startTime = new Date().getTime();
	for (i = 0; i < numPoints - 1; i++ ) {
		//Use the bits from one Math.random() call a few time, since we just need ints 
		if (i % 4 == 0) {
			rand = Math.random();
			// throw away the first bunch so the ones we keep are all nicely converged
			if (discard && i == discardCount) { 
				discard = false;
				points[0] = x;
				points[1] = y;
				points[2] = z;
				points[3] = w;
				i = 0;
			}
		}
		rand = rand * numTransforms; // Rand was between 0 and 1
		rint = rand | 0; // Math.floor(), now rint is an integer between 0 and numTransforms - 1
		rand = rand - rint; // Just leave the fractional part in rand for use next time through.
		t = transforms[rint];
		start = i * 4;
		x = points[start];
		y = points[start + 1];
		z = points[start + 2];
		w = points[start + 3];
		points[start + 4] = t[0] * x + t[4] * y + t[8] * z + t[12] * w;
		points[start + 5] = t[1] * x + t[5] * y + t[9] * z + t[13] * w;
		points[start + 6] = t[2] * x + t[6] * y + t[10] * z + t[14] * w;
		points[start + 7] =	t[3] * x + t[7] * y + t[11] * z + t[15] * w;
		//console.log ("(" + x + ", " + y + ", " + z + ", " + w + ")");
	}
	var time = new Date().getTime() - startTime;
	console.log("Calculated " + numPoints + " points in " + time + "ms.");
	
	return {
		points: points,
		numPoints: numPoints
	}
}

var Renderer = function(canvas, fractal) {
	var gl,
		mvMatrix = mat4.create(),
		pMatrix = mat4.create(),
		lightMatrix = mat3.create(),
        spinMatrix = mat4.create(),
        rotationMatrix = mat4.create(),
		lightAngle = 0,
		shaderProgram,
		pointBuffer,
		lightAngle;

    mat4.identity(spinMatrix);
    mat4.identity(rotationMatrix);
		
	function initGL() {
	    try {
            gl = canvas.getContext("experimental-webgl");
            gl.clearColor(0.0, 0.0, 0.0, 0.2);  
        } catch (e) { }
        if (!gl) {
            alert("Could not initialise WebGL, sorry :-(");
        }
	}
	
	function getShader(gl, id) {
		var shaderScript = document.getElementById(id);
        if (!shaderScript) {
            return null;
        }

        var str = "";
        var k = shaderScript.firstChild;
        while (k) {
            if (k.nodeType == 3) {
                str += k.textContent;
            }
            k = k.nextSibling;
        }

        var shader;
        if (shaderScript.type == "x-shader/x-fragment") {
            shader = gl.createShader(gl.FRAGMENT_SHADER);
        } else if (shaderScript.type == "x-shader/x-vertex") {
            shader = gl.createShader(gl.VERTEX_SHADER);
        } else {
            return null;
        }

        gl.shaderSource(shader, str);
        gl.compileShader(shader);

        if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
            alert(gl.getShaderInfoLog(shader));
            return null;
        }

        return shader;
    }

    function initShaders() {
        var fragmentShader = getShader(gl, "shader-fs");
        var vertexShader = getShader(gl, "shader-vs");

        shaderProgram = gl.createProgram();
        gl.attachShader(shaderProgram, vertexShader);
        gl.attachShader(shaderProgram, fragmentShader);
        gl.linkProgram(shaderProgram);

        if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
            alert("Could not initialise shaders");
        }

        gl.useProgram(shaderProgram);

        shaderProgram.vertexPositionAttribute = gl.getAttribLocation(shaderProgram, "aVertexPosition");
        gl.enableVertexAttribArray(shaderProgram.vertexPositionAttribute);

        shaderProgram.pMatrixUniform = gl.getUniformLocation(shaderProgram, "uPMatrix");
        shaderProgram.mvMatrixUniform = gl.getUniformLocation(shaderProgram, "uMVMatrix");
        shaderProgram.lightPosition = gl.getUniformLocation(shaderProgram, "lightPosition");
    }

    function setMatrixUniforms() {
        gl.uniformMatrix4fv(shaderProgram.pMatrixUniform, false, pMatrix);
        gl.uniformMatrix4fv(shaderProgram.mvMatrixUniform, false, mvMatrix);
        lightMatrix[0] = 0.6 * Math.sin(lightAngle);
        lightMatrix[1] = 1.6 * Math.cos(lightAngle);
        lightMatrix[2] = -0.6 * Math.cos(lightAngle);
        
        lightMatrix[3] = -1.7 * Math.sin(lightAngle * 0.4 + 1.2);
        lightMatrix[4] = 0.7 * Math.cos(lightAngle * 0.4 + 1.2);
        lightMatrix[5] = 0.7 * Math.cos(lightAngle * 0.4 + 1.2);
        
        lightMatrix[6] = 0.6 * Math.sin(lightAngle * 1.9 - 7.0);
        lightMatrix[7] = 0.6 * Math.cos(lightAngle * 1.9 - 7.0);
        lightMatrix[8] = 1.6 * Math.cos(lightAngle * 1.9 - 7.0)
		gl.uniformMatrix3fv(shaderProgram.lightPosition, false, lightMatrix);
    }

    function initBuffers() {
        pointBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, pointBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(fractal.points), gl.STATIC_DRAW);
        pointBuffer.itemSize = 4;
        pointBuffer.numItems = fractal.numPoints;
        gl.vertexAttribPointer(shaderProgram.vertexPositionAttribute, pointBuffer.itemSize, gl.FLOAT, false, 0, 0);
    }
	
    function drawScene() {
        gl.viewport(0, 0, gl.viewportWidth, gl.viewportHeight);
        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

        mat4.perspective(45, gl.viewportWidth / gl.viewportHeight, 0.1, 100.0, pMatrix);

        mat4.identity(mvMatrix);

        mat4.translate(mvMatrix, [0.0, 0.0, -4.0]);
  
        // apply spin velocity to rotation matrix
        mat4.multiply(rotationMatrix, spinMatrix);
        // then apply rotation matrix to model view
        mat4.multiply(mvMatrix, rotationMatrix);
        setMatrixUniforms();
		lightAngle += 0.1;
        gl.drawArrays(gl.POINTS, 0, pointBuffer.numItems);
    }

    function spin(dX, dY) {
        var ir = mat4.create; // inverse rotation matrix
        mat4.inverse(rotationMatrix, ir);
        var xAxis = [ir[0],ir[1],ir[2]];
        var yAxis = [ir[4],ir[5],ir[6]];
        
        mat4.rotate(spinMatrix,dX,yAxis);
        mat4.rotate(spinMatrix,dY,xAxis);
    }

    function initInput() {
        document.onkeydown = function(e) { 
           switch(e.keyCode) {
              case 37: spin(-0.01, 0); //left
                break;
              case 39: spin(0.01, 0); //right
                break;
              case 38: spin(0, -0.01); //up
                break;
              case 40: spin(0, 0.01); //down
                break;
              case 32: mat4.identity(spinMatrix); //space
                break;
           }
        };
        var mc = new Hammer.Manager(canvas, {
            recognizers: [
                [Hammer.Tap],
                [Hammer.Swipe,{ direction: Hammer.DIRECTION_ALL }]
            ]
        });
        mc.on("swipe", function(ev) {
            spin( ev.velocityX / 20, ev.velocityY / 20 );
        });
        mc.on("tap", function(ev) {
            // stop this crazy thing, I want to get off!
            mat4.identity(spinMatrix);
        });
    }

    function setSize() {
        var x = window.innerWidth - 8,
            y = window.innerHeight - 8;
        gl.viewportWidth = canvas.width = x;
        gl.viewportHeight = canvas.height = y;
    }

    function start() {
        initGL(canvas);
        setSize();
        window.addEventListener("resize", setSize);
        initShaders();
        initBuffers();
        initInput();
        gl.clearColor(0.0, 0.0, 0.0, 1.0);
        gl.disable(gl.DEPTH_TEST);
		gl.enable(gl.BLEND);
		gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
        drawScene();
    	setInterval(function() {drawScene();}, 50); //20fps
    }
    
	return {
		start: start 
	}
} 
