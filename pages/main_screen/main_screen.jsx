import { StatusBar } from "expo-status-bar";
import {
  StyleSheet,
  Text,
  View,
  ImageBackground,
  TouchableOpacity,
  ScrollView,
} from "react-native";
import { BlurView } from "expo-blur";
import { SvgXml } from "react-native-svg";
import { notification_none, mini_logo } from "../../images/images";
import { useNavigation } from "@react-navigation/native";
import BurgerMenu from "./burger_menu";
import { useState, useEffect } from "react";
import { useStores } from "../../store/store_context";

import Room_1 from "../../components/room_1";
import Room_2 from "../../components/room_2";
import Room_3 from "../../components/room_3";
import Room_4 from "../../components/room_4";

const MainScreen = ({ route }) => {
  const { routeStore } = useStores();
  useEffect(() => {
    routeStore.updateRoute(route);
  }, []);
  const navigation = useNavigation();
  const [colorButton, setColorButton] = useState(0);
  const [component, setComponent] = useState(<Room_1 />);
  const handleButtonClick = (index) => {
    setColorButton(index);
  };

  return (
    <View style={styles.container}>
      <StatusBar style="light" />
      <ImageBackground
        source={require("./../../images/stars_background.png")}
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          alignself: "center",
        }}
        resizeMode="cover"
      >
        <ScrollView
          style={{ width: "100%" }}
          showsVerticalScrollIndicator={false}
        >
          <BurgerMenu color_burger="white" />
          <View
            style={{ marginTop: 40, display: "flex", alignItems: "center" }}
          >
            <SvgXml xml={mini_logo} />
          </View>
          <TouchableOpacity
            onPress={() => navigation.navigate("NotificationScreen")}
            style={{
              display: "flex",
              flexDirection: "row",
              justifyContent: "space-between",
              position: "absolute",
              top: 60,
              left: 20,
            }}
          >
            <SvgXml xml={notification_none} />
          </TouchableOpacity>
          <BlurView
            intensity={17}
            borderRadius="25"
            style={styles.booking_window}
          >
            <Text
              style={{
                color: "white",
                fontSize: 20,
                marginTop: 15,
                textAlign: "center",
                fontFamily: "DelaGothicOneRegular",
              }}
            >
              Забронируйте столик
            </Text>
            <View style={styles.datetime_view}>
              <View style={{ width: "50%" }}>
                <Text style={styles.subheaders}>Дата</Text>
                <TouchableOpacity style={styles.datetime_button}>
                  <Text
                    style={[
                      styles.datetime_text,
                      styles.padding_datetime_button,
                    ]}
                  >
                    30.04.2024
                  </Text>
                </TouchableOpacity>
              </View>
              <View style={{ width: "50%" }}>
                <Text style={styles.subheaders}>Время</Text>
                <TouchableOpacity style={styles.datetime_button}>
                  <Text
                    style={[
                      styles.datetime_text,
                      styles.padding_datetime_button,
                    ]}
                  >
                    19:00
                  </Text>
                </TouchableOpacity>
              </View>
            </View>
            <View style={{ marginTop: 10, gap: 5 }}>
              <Text style={[styles.subheaders]}>Зал</Text>
              <View style={styles.tables_view}>
                <TouchableOpacity
                  onPress={() => {
                    handleButtonClick(0);
                    setComponent(<Room_1 />);
                  }}
                  style={[
                    styles.table_button,
                    colorButton === 0
                      ? { backgroundColor: "rgba(10, 185, 180, 1)" }
                      : {},
                  ]}
                >
                  <Text
                    style={[
                      styles.table_text,
                      colorButton === 0
                        ? { color: "white" }
                        : { color: "rgba(10, 185, 180, 1)" },
                    ]}
                  >
                    ЗАЛ "САКУРА"
                  </Text>
                </TouchableOpacity>
                <TouchableOpacity
                  onPress={() => {
                    handleButtonClick(1);
                    setComponent(<Room_2 />);
                  }}
                  style={[
                    styles.table_button,
                    colorButton === 1
                      ? { backgroundColor: "rgba(10, 185, 180, 1)" }
                      : {},
                    ,
                  ]}
                >
                  <Text>
                    <Text
                      style={[
                        styles.table_text,
                        colorButton === 1
                          ? { color: "white" }
                          : { color: "rgba(10, 185, 180, 1)" },
                      ]}
                    >
                      ЗАЛ "ЕНОТ"
                    </Text>
                  </Text>
                </TouchableOpacity>
              </View>
              <View style={styles.tables_view}>
                <TouchableOpacity
                  style={[
                    styles.table_button,
                    colorButton === 2
                      ? { backgroundColor: "rgba(10, 185, 180, 1)" }
                      : {},
                  ]}
                  onPress={() => {
                    handleButtonClick(2);
                    setComponent(<Room_3 />);
                  }}
                >
                  <Text
                    style={[
                      styles.table_text,
                      colorButton === 2
                        ? { color: "white" }
                        : { color: "rgba(10, 185, 180, 1)" },
                    ]}
                  >
                    ВИП "ДЕНЬ"
                  </Text>
                </TouchableOpacity>
                <TouchableOpacity
                  onPress={() => {
                    handleButtonClick(3);
                    setComponent(<Room_4 />);
                  }}
                  style={[
                    styles.table_button,
                    colorButton === 3
                      ? { backgroundColor: "rgba(10, 185, 180, 1)" }
                      : {},
                  ]}
                >
                  <Text
                    style={[
                      styles.table_text,
                      colorButton === 3
                        ? { color: "white" }
                        : { color: "rgba(10, 185, 180, 1)" },
                    ]}
                  >
                    ВИП "НОЧЬ"
                  </Text>
                </TouchableOpacity>
              </View>
            </View>
            <View style={{ marginTop: 10 }}>
              <Text style={styles.subheaders}>Выберите свободный столик</Text>
            </View>
            <View>{component}</View>

            <TouchableOpacity
              style={[{ marginTop: 15, marginBottom: 15 }]}
              disabled={true}
            >
              <View
                style={[
                  {
                    borderRadius: 10,
                    backgroundColor: "rgba(40,40,40,1)",
                  },
                ]}
              >
                <Text
                  style={[
                    {
                      fontSize: 16,
                      width: "100%",
                      textAlign: "center",
                      paddingVertical: 20,
                      color: "white",
                      fontFamily: "ManropeSemiBold",
                    },
                  ]}
                >
                  Продолжить бронирование
                </Text>
              </View>
            </TouchableOpacity>
          </BlurView>
        </ScrollView>
      </ImageBackground>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: "100%",
    height: "100%",
    backgroundColor: "rgba(14, 74, 74, 1)",
  },
  booking_window: {
    marginTop: 20,
    borderColor: "white",
    borderWidth: 1,
    borderRadius: 25,
    paddingHorizontal: 15,
    overflow: "hidden",
    marginBottom: 80,
    marginHorizontal: 20,
  },
  datetime_view: {
    flexDirection: "row",
    justifyContent: "space-between",
    gap: 5,
    display: "flex",
    width: "100%",
    marginTop: 10,
  },
  subheaders: {
    color: "rgba(255,255,255,0.5)",
    fontSize: 12,
    fontFamily: "ManropeSemiBold",
  },
  datetime_text: {
    color: "white",
    fontSize: 12,
    fontFamily: "ManropeSemiBold",
  },
  datetime_button: {
    backgroundColor: "rgba(255, 255, 255, 0.1)",
    borderRadius: 5,
    marginTop: 5,
  },
  padding_datetime_button: {
    paddingVertical: 10,
    paddingLeft: 10,
  },
  table_text: {
    fontSize: 12,
    textAlign: "center",
    fontFamily: "DelaGothicOneRegular",
  },
  tables_view: {
    flexDirection: "row",
    width: "100%",
    gap: 5,
  },
  table_button: {
    width: "50%",
    paddingHorizontal: 15,
    paddingVertical: 5,
    borderRadius: 5,
    borderWidth: 1,
    borderColor: "rgba(10, 186, 181, 1)",
  },
});

export default MainScreen;
