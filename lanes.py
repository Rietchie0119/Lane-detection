import cv2
import numpy as np
import matplotlib.pyplot as plt

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = int(image.shape[0])
    y2 = int(y1*(3/5)) # 이미지에 라인을 그려내기 위해서는 점 두개의 좌표가 필요함 y1은 가장 밑, y2는 중간에서 약간 아래로 설정
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return [[x1, y1, x2, y2]]

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    if lines is None:
        return None
    for line in lines:
        for x1, y1, x2, y2 in line:
            parameters = np.polyfit((x1, x2), (y1, y2), 1) # 이 함수는 polynomial 형태에서 coefficients 를 반환해줌. 1은 1차 함수라는 뜻. 즉 m 과 b 를 반환
            slope = parameters[0]
            intercept = parameters[1]
            if slope < 0:
                left_fit.append((slope, intercept)) # 차량 왼쪽에 선이 존재함
            else:
                right_fit.append((slope, intercept)) # 차량 우측에 선이 존재함
    left_fit_average = np.average(left_fit, axis= 0) # 왼쪽 선들을 axis = 0 기준, 즉 array의 행 기준으로 평균을 구함
    right_fit_average = np.average(right_fit, axis= 0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return [left_line, right_line]

# cvtColor를 적용함으로써 흑백 사진으로 변환. 연산을 줄일 수 있음.
# 가우시안 블러를 적용함으로써 weighted average, 즉 노이즈를 제거
# canny에서 자동적으로 가우시안 블러를 처리. 도큐멘테이션에선
# low-threshold 와 high-threshold는 2배 또는 3배 적용을 권장. 따라서 50과 150을 적용.
# canny: derivative(색상의 변화율)가 high threshold를 넘을때 하얀색 선으로 나타냄. low threshold와 high threshold 사이에 있을때는 high threshold를 넘는
# 선과 이어져 있을때만 하얀색으로 표시.
def canny(lane_image):
    gray = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0) #kernel size = 5 x 5
    canny = cv2.Canny(gray, 50, 150)
    return canny

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line: # 각 라인의 두개의 점을 추출
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10) #각 라인을 두께 10인 파란색으로 칠
    return line_image


def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([[(200, height), (1100, height), (550, 250)]], np.int32)
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

cap = cv2.VideoCapture("test2.mp4")
while(cap.isOpened()):
    _, frame = cap.read()
    canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)

    # 허프 변환. 데카르트 좌표계의 점x, y를 m과 b 사이의 선으로 변환할 수 있음. 하지만 극좌표계를 사용할 것이므로 로와 쎄타의 공간으로 변환.
    # Bin 에 intersection 포인트를 저장하고 가장 많은 bin의 rho, theta가 데카르트 좌표계의 점들을 잇는 선의 방정식을 나타냄.
    # 여기서 사용된 인자 2 와 pi / 180 이란 사진의 2픽셀, 1도의 오차범위를 나타내는 의미. 즉 Bin 의 크기가 rho = 2, theta = 1 란 뜻.
    # 네번째 인자는 bin안에 몇개의 intersection 이 있어야 데카르트 좌표계에서 선으로 인정하는 threshold임. 즉 최소 100 픽셀이 데카르트 좌표계에서 같은
    # 선상에 있어야 선으로 인정 된다는 뜻.
    # minLineLength 는 선으로 인정되기 위한 최소 길이 즉 40픽셀. maxLineGap는 선과 선 사이의 갭이 있을 경우 5픽셀 이하라면 같은 선으로 쳐준다.
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap = 5)
    averaged_lines = average_slope_intercept(frame, lines)

    line_image = display_lines(frame, averaged_lines) # 라인이 그려진 검은색 사진
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1) # weighted sum을 구해 이미지 두개를 합침. 마지막 1은 감마값으로 무시해도 됨.
    cv2.imshow("result", combo_image)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release() # 비디오 파일 close
cv2.destroyAllWindows() # 윈도우 끄기