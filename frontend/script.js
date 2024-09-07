const collectData = () => {
	let pointsX = []
	let pointsY = []
	let times = []
	let startTime = null

	const throttle = (func, delay) => {
		let lastCall = 0
		startTime = new Date().getTime()
		console.log(new Date(startTime + 5.5 * 60 * 60 * 1000).toUTCString())
		return function (...args) {
			const now = new Date().getTime()
			if (now - lastCall >= delay) {
				lastCall = now
				return func(...args)
			}
		}
	}

	function logMousePosition(e) {
		const x = e.clientX - drawCanvas.offsetLeft
		const y = drawCanvas.getBoundingClientRect().height - e.clientY
		let time = (new Date().getTime() - startTime) / 1000
		console.log(x, y, ' at time', time)
		pointsX.push(x)
		pointsY.push(y)
		times.push(time)
	}

	const throttledLogMousePosition = throttle(logMousePosition, 10)
	drawCanvas.addEventListener('mousemove', throttledLogMousePosition)

	setTimeout(async () => {
		drawCanvas.removeEventListener('mousemove', throttledLogMousePosition)
		console.log('Mouse movement tracking stopped.')
		console.log(pointsX, pointsY)
		console.log(times)

		const res = await fetch('http://127.0.0.1:5000/movement-data', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				x: pointsX,
				y: pointsY,
				time: times,
			}),
		})

		const blob = await res.blob()

		const url = window.URL.createObjectURL('/index.html')
		const a = document.createElement('a')
		a.href = url
		a.download = 'data.csv'
		document.body.appendChild(a)
		a.click()
		a.remove()

	}, 30 * 1000)
}

document.querySelector('button').addEventListener('click', collectData)
