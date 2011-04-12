
def upperRoundRect(x,y,w,h,r):
	return " ".join([unicode(x) for x in ["M",x+w-r,y,"a",r,r,90,0,1,r,r,"V",y+h,"h",-w,"V",y+r,"a",r,r,90,0,1,r,-r]])

def lowerRoundRect(x,y,w,h,r):
	return " ".join([unicode(x) for x in ["M",x+w,y,"v",h-r,"a",r,r,90,0,1,-r,r,"H",x+r,"a",r,r,90,0,1,-r,-r,"V",y,"H",w]])

def arrow(x,y,a,b):
	c = (a*a+b*b)**0.5
	(cos,sin) = (a/c,b/c)
	return " ".join([unicode(x) for x in [
		"M",x,y,
		"L",x+arrowWidth*cos-arrowHalfHeight*sin,y-arrowHalfHeight*cos-arrowWidth*sin,
		"L",x+arrowAxis*cos,y-arrowAxis*sin,
		"L",x+arrowWidth*cos+arrowHalfHeight*sin,y+arrowHalfHeight*cos-arrowWidth*sin,
		"Z"
	]])
