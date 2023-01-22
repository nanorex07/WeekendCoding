const size = 20
const density = 40

let canv = document.getElementById('canvas')
let ctx = canv.getContext("2d")
let framesPerSecond = 30
let running = true

canv.width = size*density
canv.height = size*density



let map = new Array()
for (let i = 0; i < density; i++) {
	let row = new Array()
	for(let j = 0; j < density; j++)
		row.push(0);
	map.push(row)
}


class Snake {
	constructor(xx, yy) {
		this.dir = {y: 0, x: 1}
		this.body = [[xx,yy]]
		map[xx][yy] = 1
	}
 	
 	check(x, y) {
 		if (x < 0 || x >= density) return false;
 		if (y < 0 || y >= density) return false;
 		return true;	
 	}

	move() {
		let newPos = [this.body[this.body.length - 1][0] + this.dir.y,
this.body[this.body.length - 1][1] + this.dir.x]

		if (this.check(newPos[0], newPos[1]) == false || 
				map[newPos[0]][newPos[1]] == 1
			) {
			running = false
			return
		}
		console.log(this.dir)

		let ff = this.body.shift()
		this.body.push(newPos)
		map[ff[0]][ff[1]] = 0
		map[newPos[0]][newPos[1]] = 1
	}
}
class Food {
	constructor(a, b) {
		this.a = a
		this.b = b
		map[this.a][this.b] = 2;
	}
	new() {
		this.a = Math.floor(Math.random()*density)
		this.b = Math.floor(Math.random()*density)
		map[this.a][this.b] = 2
	}
}



let draw_map = ()=>{
	ctx.strokeStyle = "white"
	ctx.lineWidth=size/20
	for(let i = 0; i < density; i++) {
		for(let j = 0; j < density; j++){
			if (map[i][j] == 0) {
				ctx.fillStyle = "black"
			} else if (map[i][j] == 1) {
				ctx.fillStyle = "blue"
			} else{
				ctx.fillStyle = "red"
			}
			ctx.fillRect(size*j, size*i, size,size)
			// ctx.strokeRect(size*j, size*i, size,size)

		}
	}
}

let snake = new Snake(Math.floor(density/2), 0)
let food = new Food(4,5)

window.addEventListener('keydown',(e)=>{
	let code = e.keyCode
	//up
	if ((code == 87 || code == 38) && snake.dir.y != 1){
		snake.dir.x = 0
		snake.dir.y = -1
	}
	//down
	else if ((code == 83 || code == 40) && snake.dir.y != -1){
		snake.dir.x = 0
		snake.dir.y = 1
	}
	//left
	else if ((code == 65 || code == 37) && snake.dir.x != 1){
		snake.dir.y = 0
		snake.dir.x = -1
	}
	//right
	else if ((code == 68 || code == 39) && snake.dir.x != -1){
		snake.dir.x = 1
		snake.dir.y = 0
	}
},false);

let eat = ()=>{
	if (snake.body[snake.body.length-1][0] == food.a && snake.body[snake.body.length-1][1] == food.b){
		snake.body.push([food.a, food.b])
		map[food.a][food.b] = 1
		food.new()
	}
}

let loop = ()=>{
	setTimeout(function() {
        requestAnimationFrame(loop);
        if (running) {
			draw_map()
			snake.move()
			eat()
    	}

    }, 1000 / framesPerSecond);

}

loop()

