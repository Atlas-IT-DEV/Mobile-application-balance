import { useNavigation } from "@react-navigation/native";
import { Formik } from "formik";
import { TouchableOpacity } from "react-native";
import { StyleSheet, Text, TextInput, View } from "react-native";

const LoginForm = () => {
  const navigation = useNavigation();
  return (
    <Formik>
      <View style={styles.container}>
        <Text style={styles.namePageText}>Войти в профиль</Text>

        <View style={styles.inputsView}>
          <TextInput
            style={styles.input}
            keyboardType="number-pad"
            placeholder="+7 000 000 00 00"
            placeholderTextColor={"rgba(183, 183, 183, 1)"}
          />

          <TextInput
            style={styles.input}
            keyboardType="default"
            placeholder="Пароль"
            placeholderTextColor={"rgba(183, 183, 183, 1)"}
          />
        </View>
        <TouchableOpacity
          style={styles.loginButton}
          onPress={() => navigation.navigate("MainScreen")}
        >
          <Text style={styles.loginButtonText}>Войти</Text>
        </TouchableOpacity>
        <Text style={styles.aboutProfileText}>Нет профиля?</Text>
        <TouchableOpacity
          style={styles.enterButton}
          onPress={() => navigation.navigate("RegistrationScreen")}
        >
          <Text style={styles.enterButtonText}>Пройти регистрацию</Text>
        </TouchableOpacity>
      </View>
    </Formik>
  );
};

const styles = StyleSheet.create({
  container: {
    width: "100%",
    height: "100%",
    backgroundColor: "white",
  },
  namePageText: {
    color: "rgba(22, 3, 111, 1)",
    fontFamily: "IBMSemiBold",
    fontSize: 22,
    alignSelf: "center",
  },
  inputsView: {
    paddingHorizontal: 68,
    marginTop: 30,
    gap: 15,
  },
  input: {
    backgroundColor: "rgba(255,255,255,1)",
    borderRadius: 10,
    shadowColor: "rgba(36, 27, 79, 0.2)",
    shadowOffset: {
      width: 0,
      height: 0,
    },
    shadowOpacity: 1,
    shadowRadius: 8,
    height: 40,
    paddingHorizontal: 20,
  },
  loginButton: {
    height: 40,
    backgroundColor: "rgba(48, 31, 129, 1)",
    marginHorizontal: 68,
    marginTop: 15,
    justifyContent: "center",
    alignItems: "center",
    borderRadius: 10,
  },
  loginButtonText: {
    color: "white",
    fontFamily: "IBMSemiBold",
  },
  aboutProfileText: {
    alignSelf: "center",
    marginTop: 15,
    fontFamily: "IBMMedium",
    color: "rgba(113, 113, 113, 1)",
  },
  enterButton: {
    alignItems: "center",
    marginTop: 10,
  },
  enterButtonText: {
    color: "rgba(22, 3, 111, 1)",
    fontFamily: "IBMMedium",
  },
});
export default LoginForm;
