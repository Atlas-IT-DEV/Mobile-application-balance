import { SafeAreaView, ScrollView, StyleSheet, Text, View } from "react-native";
import { SvgXml } from "react-native-svg";
import { logo } from "../../images/images";
import LoginForm from "../../components/forms/login_form";

const LoginScreen = () => {
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView automaticallyAdjustKeyboardInsets={true}>
        <View style={styles.logo}>
          <SvgXml xml={logo} />
          <Text style={styles.logoText}>БЛАГОТВОРИТЕЛЬНЫЙ ФОНД</Text>
        </View>
        <View style={styles.form}>
          <LoginForm />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    width: "100%",
    height: "100%",
    backgroundColor: "white",
  },
  logo: {
    alignItems: "center",
    opacity: 0.5,
    marginTop: 30,
    gap: 2,
  },
  logoText: {
    color: "rgba(45, 22, 153, 1)",
    fontFamily: "IBMMedium",
    fontSize: 10,
  },
  form: {
    marginTop: 138,
  },
});
export default LoginScreen;
