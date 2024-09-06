import { Text, View, StyleSheet } from "react-native";

import { SvgXml } from "react-native-svg";
import { TouchableOpacity } from "react-native";
import { useNavigation } from "@react-navigation/native";
import { useState } from "react";
import {
  homeActiveIcon,
  homeIcon,
  notificationActiveIcon,
  notificationIcon,
  profileActiveIcon,
  profileIcon,
} from "../images/images";

const BottomMenu = () => {
  const [selected, setSelected] = useState([0, 1, 0]);
  const navigation = useNavigation();

  return (
    <View style={styles.container}>
      <TouchableOpacity
        style={styles.button}
        onPress={() => {
          setSelected([1, 0, 0]);
        }}
      >
        <SvgXml xml={selected[0] == 1 ? profileActiveIcon : profileIcon} />
        <Text
          style={[
            styles.buttonText,
            selected[0] == 1 ? styles.activeText : styles.unActiveText,
          ]}
        >
          Профиль
        </Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={styles.button}
        onPress={() => {
          setSelected([0, 1, 0]);
        }}
      >
        <SvgXml xml={selected[1] == 1 ? homeActiveIcon : homeIcon} />
        <Text
          style={[
            styles.buttonText,
            selected[1] == 1 ? styles.activeText : styles.unActiveText,
          ]}
        >
          Главная
        </Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={styles.button}
        onPress={() => {
          setSelected([0, 0, 1]);
        }}
      >
        <SvgXml
          xml={selected[2] == 1 ? notificationActiveIcon : notificationIcon}
        />
        <Text
          style={[
            styles.buttonText,
            selected[2] == 1 ? styles.activeText : styles.unActiveText,
          ]}
        >
          Уведомления
        </Text>
      </TouchableOpacity>
    </View>
  );
};
const styles = StyleSheet.create({
  container: {
    width: "100%",
    height: 60,
    backgroundColor: "white",
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    position: "absolute",
    bottom: 0,
    left: 0,
    paddingHorizontal: 52,
    gap: 60,
    // shadowColor: "rgba(36, 27, 79, 0.2)",
    shadowOffset: {
      width: 2,
      height: 2,
    },
    shadowOpacity: 0.2,
    shadowRadius: 20,
  },
  button: {
    alignItems: "center",
    gap: 3,
  },
  buttonText: {
    fontFamily: "IBMMedium",
    fontSize: 12,
  },
  activeText: {
    color: "rgba(22, 3, 111, 1)",
  },
  unActiveText: {
    color: "rgba(113, 113, 113, 1)",
  },
});

export default BottomMenu;
