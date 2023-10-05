#! /usr/bin/env python3
import os
import rospy
import rospkg
from visualization_msgs.msg import MarkerArray, Marker

rospy.init_node("object_visualizer")
rate = rospy.Rate(0.5)
rospy.loginfo('Initializing object visualizer')
rp = rospkg.RosPack()
visualizer_path = os.path.join(rp.get_path('object_visualizer'), 'meshes')

visualizer_path = rospy.get_param("~visualizer_path", visualizer_path)
frame = rospy.get_param("~frame", "map")

markerArray = MarkerArray()

publisher = rospy.Publisher('visualization_marker', MarkerArray, queue_size=1)

current_file_count = 0
while not rospy.is_shutdown():
    files = [file for file in os.listdir(visualizer_path) if file.endswith(('.dae', '.stl', '.mesh'))]  # find all meshes in the 'meshes' folder
    if len(files) != current_file_count:  # if the number of valid meshed in the 'meshes' folder has changed
        if len(files) < current_file_count:  # if some markers are removed from the 'meshes' folder, delete them in RViz
            marker = Marker()
            marker.header.frame_id = frame
            marker.action = marker.DELETEALL # send the DELETEALL marker to delete all marker in RViz
            markerArray.markers.append(marker)
            publisher.publish(markerArray)

        current_file_count = len(files)
        for marker_id, file in enumerate(files):
            rospy.loginfo('Loading file: %s', file)
            marker = Marker()
            marker.id = marker_id
            marker.mesh_resource = "file://" + visualizer_path + "/" + file
            marker.mesh_use_embedded_materials = True  # Need this to use textures for mesh
            marker.type = marker.MESH_RESOURCE
            marker.header.frame_id = frame
            marker.scale.x = 1.0
            marker.scale.y = 1.0
            marker.scale.z = 1.0
            marker.pose.orientation.w = 1.0
            markerArray.markers.append(marker)

    # rospy.loginfo('Published %d objects. ', len(markerArray.markers))
    publisher.publish(markerArray)
    rate.sleep()
