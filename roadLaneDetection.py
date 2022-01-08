import cv2
import numpy as np

cap = cv2.VideoCapture("solidWhiteRight.mp4")


if not cap.isOpened():
    print("cannot open input video")
    exit()

img_size = [200, 360]
src = np.float32([[10, 200],
                 [350, 200],
                 [215, 120],
                 [120, 120]])
scr_draw = np.array(src, dtype=np.int32)

dst = np.float32([[0, img_size[0]],
                 [img_size[1], img_size[0]],
                 [img_size[1], 0],
                 [0, 0]])

while cv2.waitKey(10) != 27:
    ret, frame = cap.read()
    if not ret:
        print("End of video")
        break
    resized = cv2.resize(frame, (img_size[1], img_size[0]))
    cv2.imshow("original", resized)

    r_channel = resized[:, :, 2]
    binary = np.zeros_like(r_channel)
    binary[r_channel > 200] = 1
    cv2.imshow("r_chan", binary)
    # edges = cv2.Canny(resized, 500, 700)
    # cv2.imshow('edges', edges)
    hls = cv2.cvtColor(resized, cv2.COLOR_BGR2HLS)
    s_channel = resized[:, :, 2]
    binary2 = np.zeros_like(s_channel)
    binary2[s_channel > 160] = 1
    cv2.imshow("s_chan", binary2)

    allBinary = np.zeros_like(binary)
    allBinary[(binary == 1) | binary2 == 1] = 255
    cv2.imshow('ALLBINARY', allBinary)

    allBinary_visual = allBinary.copy()

    cv2.polylines(allBinary_visual, [scr_draw], True, 255)
    cv2.imshow("sksjs", allBinary_visual)

    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(allBinary, M, (img_size[1], img_size[0]),
                                 flags=cv2.INTER_LINEAR
                                 )
    cv2.imshow("warped", warped)

    histogram = np.sum(warped[warped.shape[0] // 2 :, :], axis=0 )

    midPoint = histogram.shape[0] // 2
    indWhitestColumnL = np.argmax(histogram[:midPoint])
    indWhitestColumnR = np.argmax(histogram[midPoint:]) + midPoint

    warped_visual = warped.copy()
    cv2.line(warped_visual, (indWhitestColumnL, 0), (indWhitestColumnL, warped_visual.shape[0]), 110, 2 )
    cv2.line(warped_visual, (indWhitestColumnR, 0), (indWhitestColumnR, warped_visual.shape[0]), 110, 2 )
    cv2.imshow("warped visual", warped_visual)

    nwindows = 19
    window_height = int(warped.shape[0] / nwindows)
    window_half_width = 25
    XCenterLeftWin = indWhitestColumnL
    XCenterRightWin = indWhitestColumnR

    left_lane_inds = np.array([], dtype=np.int16)
    right_lane_inds = np.array([], dtype=np.int16)

    out_img = np.dstack((warped, warped, warped))
    nonzero = warped.nonzero()
    WhitePixelY = np.array(nonzero[0])
    WhitePixelX = np.array(nonzero[1])

    for window in range(nwindows):
        win_y1 = warped.shape[0] - (window + 1) * window_height
        win_y2 = warped.shape[0] - (window) * window_height

        left_win_x1 = XCenterLeftWin - window_half_width
        left_win_x2 = XCenterLeftWin + window_half_width
        right_win_x1 = XCenterRightWin - window_half_width
        right_win_x2 = XCenterRightWin + window_half_width

        cv2.rectangle(out_img, (left_win_x1, win_y1), (left_win_x2, win_y2), (214, 41, 136), 1)
        cv2.rectangle(out_img, (right_win_x1, win_y1), (right_win_x2, win_y2), (233, 174, 22), 1)
        cv2.imshow('treking with colors', out_img)
        good_left_inds = ((WhitePixelY >= win_y1) & (
                WhitePixelY <= win_y2) & (WhitePixelX >= left_win_x1) & (WhitePixelX <= left_win_x2)).nonzero()[0]
        good_right_inds = ((WhitePixelY >= win_y1) & (
                    WhitePixelY <= win_y2) & (WhitePixelX >= right_win_x1) & (WhitePixelX <= right_win_x2)).nonzero()[0]
        left_lane_inds = np.concatenate((left_lane_inds, good_left_inds))
        right_lane_inds = np.concatenate((right_lane_inds, good_right_inds))
    out_img[WhitePixelY[left_lane_inds], WhitePixelX[left_lane_inds]] = [255, 0, 0]
    out_img[WhitePixelY[right_lane_inds], WhitePixelX[right_lane_inds]] = [0, 0, 255]
    cv2.imshow('lane', out_img)