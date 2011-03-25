
def cardPos(ex,ey,ew,eh,ax,ay,k):
	if ax!=ex and abs(float(ay-ey)/(ax-ex)) < float(eh)/ew:
		(x0,x1) = (ex+cmp(ax,ex)*(ew+cardMargin), ex+cmp(ax,ex)*(ew+cardMargin+cardMaxWidth))
		(y0,y1) = sorted([ey+(x0-ex)*(ay-ey)/(ax-ex), ey+(x1-ex)*(ay-ey)/(ax-ex)])
		return (min(x0,x1),(y0+y1-cardMaxHeight+k*abs(y1-y0+cardMaxHeight))/2+cmp(k,0)*cardMargin)
	else:
		(y0,y1) = (ey+cmp(ay,ey)*(eh+cardMargin), ey+cmp(ay,ey)*(eh+cardMargin+cardMaxHeight))
		(x0,x1) = sorted([ex+(y0-ey)*(ax-ex)/(ay-ey), ex+(y1-ey)*(ax-ex)/(ay-ey)])
		return ((x0+x1-cardMaxWidth+k*abs(x1-x0+cardMaxWidth))/2+cmp(k,0)*cardMargin,min(y0,y1))

def lineArrow(x0,y0,x1,y1,t):
	(x,y) = (t*x0+(1-t)*x1,t*y0+(1-t)*y1)
	return arrow(x,y,x1-x0,y0-y1)
	
def curveArrow(x0,y0,x1,y1,x2,y2,x3,y3,t):
	(cx,cy) = (3*(x1-x0),3*(y1-y0))
	(bx,by) = (3*(x2-x1)-cx,3*(y2-y1)-cy)
	(ax,ay) = (x3-x0-cx-bx,y3-y0-cy-by)
	t = 1-t
	bezier  = lambda t: (ax*t*t*t + bx*t*t + cx*t + x0, ay*t*t*t + by*t*t + cy*t + y0)
	(x,y) = bezier(t)
	u = 1.0
	while t < u:
		m = (u+t)/2.0
		(xc,yc) = bezier(m)
		d = ((x-xc)**2+(y-yc)**2)**0.5
		if abs(d-arrowAxis) < 0.01:
			break
		if d > arrowAxis:
			u = m
		else:
			t = m
	return arrow(x,y,xc-x,y-yc)