import {
  StyleSheet,
  View,
  StatusBar,
  SafeAreaView,
  ScrollView,
} from "react-native";
import Header from "../../components/header";
import MiniProfileInfo from "../../components/mini_profile_info";

const MainScreen = () => {
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <ScrollView>
        <View style={styles.header}>
          <Header />
        </View>
        <View style={styles.profile}>
          <MiniProfileInfo />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    width: "100%",
    height: "100%",
  },
  header: {
    paddingHorizontal: 38,
    marginTop: 15,
  },
  profile: {
    paddingHorizontal: 20,
    marginTop: 20,
  },
});

export default MainScreen;
