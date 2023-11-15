import { ObjectData } from "@/types/objects";
import axios from "axios";
import { baseURL } from "@/api";

export async function getObjectData(
  id: string,
  name: string,
  objectIndex: string
): Promise<ObjectData> {
  return (
    await axios.get<ObjectData>(
      baseURL + "/objects/" + id + "/" + name + "/" + objectIndex
    )
  ).data;
}
