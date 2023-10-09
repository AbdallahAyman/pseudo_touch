import os
import open3d as o3d
from src.data_collection.utils import search_folder
from src.utils.utils import point_cloud_info

if __name__ == "__main__":
    # take object name from user input interactively
    object_name = input("Enter the name of the object: ")
    # take number from user input interactively
    num = input("Enter the number of the pcd file you want to filter: ")
    num = int(num)

    # get the path of this file using os.path
    path = search_folder("/", "touch2image")

    while True:
        # Load point cloud from a file
        point_cloud = o3d.io.read_point_cloud(
            f"{path}/reskin/data_collection/data/{object_name}/pcds/experiment_{num}_combined.pcd"
        )
        # radius filter on point cloud
        point_cloud.estimate_normals()
        # get point cloud info from function in ths repo
        point_cloud_info(point_cloud, display=True)

        # parameters for a dense point cloud
        point_cloud = point_cloud.voxel_down_sample(voxel_size=0.0001)
        point_cloud = point_cloud.remove_radius_outlier(nb_points=30, radius=0.001)[0]

        # visualize the point cloud
        o3d.visualization.draw_geometries([point_cloud])

        # # delete the old file
        os.remove(f"{path}/data/{object_name}/pcds/experiment_{num}_combined.pcd")
        # Save the point cloud as a .pcd file
        o3d.io.write_point_cloud(
            f"{path}/data/{object_name}/pcds/experiment_{num}_combined.pcd", point_cloud
        )
        # prompt user to continue or not
        cont = input("Do you want to continue? (y/n): ")
        if cont == "n":
            break
