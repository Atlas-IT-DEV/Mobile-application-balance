import { StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { SvgXml } from "react-native-svg";
import { arrowRightIcon } from "../images/images";

const SubscribeMiniCard = ({
  name_subscribe = "Ремонт дома для пожилой пары",
}) => {
  return (
    <TouchableOpacity style={styles.container}>
      <Text style={styles.nameText}>{name_subscribe}</Text>
      <SvgXml xml={arrowRightIcon} />
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  nameText: {
    color: "rgba(52, 52, 52, 1)",
    fontFamily: "IBMMedium",
  },
});
export default SubscribeMiniCard;
