import { BlurView } from "expo-blur";
import { StyleSheet, Text, TouchableOpacity, View } from "react-native";

const MiniProfileInfo = ({
  name = "Фамилия Имя",
  phone_number = "+7 (800) 555 35-35",
}) => {
  return (
    <View style={styles.container}>
      <View>
        <Text style={styles.nameText}>{name}</Text>
        <Text style={styles.phoneText}>{phone_number}</Text>
      </View>
      <TouchableOpacity style={styles.button}>
        <Text style={styles.buttonText}>Пополнить</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "rgba(255,255,255,1)",
    borderRadius: 20,
    shadowColor: "rgba(36, 27, 79, 0.2)",
    shadowOffset: {
      width: 3,
      height: 3,
    },
    shadowOpacity: 0.7,
    shadowRadius: 2,
  },
  nameText: {
    color: "rgba(52, 52, 52, 1)",
    fontFamily: "IBMMedium",
  },
  phoneText: {
    color: "rgba(52, 52, 52, 1)",
    fontFamily: "IBMRegular",
    fontSize: 12,
    marginTop: 5,
  },
  button: {
    height: 35,
    paddingHorizontal: 20,
    backgroundColor: "rgba(221, 27, 27, 1)",
    justifyContent: "center",
    borderRadius: 10,
  },
  buttonText: {
    color: "rgba(255, 255, 255, 1)",
    fontFamily: "IBMSemiBold",
  },
});

export default MiniProfileInfo;
