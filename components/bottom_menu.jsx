import { Text, View, StyleSheet } from "react-native";
import {
  profile_icon,
  notebook_icon,
  home_icon,
  order_icon,
} from "../images/images";
import { SvgXml } from "react-native-svg";
import { TouchableOpacity } from "react-native";
import { useNavigation } from "@react-navigation/native";
import { useState } from "react";
import { useStores } from "../store/store_context";

const BottomMenu = () => {
  const [selected, setSelected] = useState([0, 0, 0, 0]);
  const navigation = useNavigation();
  const { routeStore } = useStores();

  return (
    <View style={styles.container}>
      {routeStore.route.name == "MainScreen" ||
      routeStore.route.name == "ProfileScreen" ||
      routeStore.route.name == "MenuScreen" ||
      routeStore.route.name == "BookingScreen" ? (
        <View style={styles.content}>
          <TouchableOpacity
            onPress={() => {
              setSelected([1, 0, 0, 0]);
              navigation.navigate("ProfileScreen");
              console.log(routeStore.route.name);
            }}
            style={
              selected[0] == 1
                ? styles.selected_button_menu
                : styles.button_menu
            }
          >
            <SvgXml xml={profile_icon} />
            <Text style={[styles.button_text]}>Профиль</Text>
          </TouchableOpacity>
          <TouchableOpacity
            onPress={() => {
              setSelected([0, 1, 0, 0]);
              navigation.navigate("MenuScreen");
              console.log(routeStore.route.name);
            }}
            style={
              selected[1] == 1
                ? styles.selected_button_menu
                : styles.button_menu
            }
          >
            <SvgXml xml={notebook_icon} />
            <Text style={[styles.button_text]}>Меню</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={
              selected[2] == 1
                ? styles.selected_button_menu
                : styles.button_menu
            }
            onPress={() => {
              setSelected([0, 0, 1, 0]);
              navigation.navigate("MainScreen");
              console.log(routeStore.route.name);
            }}
          >
            <SvgXml xml={home_icon} />
            <Text style={[styles.button_text]}>Домой</Text>
          </TouchableOpacity>
          <TouchableOpacity
            onPress={() => {
              setSelected([0, 0, 0, 1]);
              navigation.navigate("BookingScreen");
              console.log(routeStore.route.name);
            }}
            style={
              selected[3] == 1
                ? styles.selected_button_menu
                : styles.button_menu
            }
          >
            <SvgXml xml={order_icon} />
            <Text style={[styles.button_text]}>Заказ</Text>
          </TouchableOpacity>
        </View>
      ) : null}
    </View>
  );
};
const styles = StyleSheet.create({
  container: {
    width: "100%",
    position: "absolute",
    bottom: 20,
  },
  content: {
    marginHorizontal: 21,
    backgroundColor: "rgba(7, 131, 132, 1)",
    borderRadius: 50,
    flexDirection: "row",
    justifyContent: "space-around",
    height: 50,
    alignItems: "center",
  },
  button_menu: {
    alignItems: "center",
    paddingVertical: 8,
    height: 42,
    justifyContent: "center",

    borderRadius: 50,
    paddingHorizontal: 15,
  },
  selected_button_menu: {
    alignItems: "center",
    paddingVertical: 8,
    height: 42,
    justifyContent: "center",
    borderRadius: 50,
    paddingHorizontal: 15,
    backgroundColor: "rgba(208, 53, 140, 1)",

    width: 80,
  },
  button_text: {
    color: "white",
    fontSize: 10,
    fontFamily: "ManropeBold",
  },
});

export default BottomMenu;
