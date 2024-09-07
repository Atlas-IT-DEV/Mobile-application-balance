import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  View,
} from "react-native";

const NotificationScreen = () => {
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <ScrollView>
        <View style={styles.namePage}>
          <Text style={styles.namePageText}>Уведомления</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    width: "100%",
    height: "100%",
    backgroundColor: "rgba(255,255,255,1)",
  },
  namePage: {
    alignItems: "center",
    marginTop: 25,
  },
  namePageText: {
    color: "rgba(22, 3, 111, 1)",
    fontSize: 22,
    fontFamily: "IBMSemiBold",
  },
});
export default NotificationScreen;
