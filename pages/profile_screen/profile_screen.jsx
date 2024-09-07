import {
  StyleSheet,
  View,
  StatusBar,
  SafeAreaView,
  ScrollView,
  Text,
  TouchableOpacity,
} from "react-native";
import { useNavigation } from "@react-navigation/native";

import SubscribeMiniCard from "../../components/subscribe_mini_card";
import ModalDeteleAccount from "../../components/modal_detete_account";

const ProfileScreen = ({
  name = "Имя",
  surname = "Фамилия",
  phone_number = "+7 (800) 555 35-35",
  inn = "8888 888 888 88",
}) => {
  const navigation = useNavigation();

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <ScrollView>
        <View style={styles.namePage}>
          <Text style={styles.namePageText}>Профиль</Text>
        </View>
        <View style={[styles.component, styles.userInfo]}>
          <View style={styles.headerProfile}>
            <Text style={styles.nameComponentText}>Информация о профиле</Text>
            <TouchableOpacity
              onPress={() => {
                navigation.navigate("EditProfileScreen");
              }}
            >
              <Text style={styles.editButtonText}>Изменить</Text>
            </TouchableOpacity>
          </View>

          <View style={styles.fields}>
            <View style={styles.divideLine} />
            <View style={styles.rowField}>
              <Text style={styles.attributeText}>Имя</Text>
              <Text style={styles.valueText}>{name}</Text>
            </View>
            <View style={styles.divideLine} />
            <View style={styles.rowField}>
              <Text style={styles.attributeText}>Фамилия</Text>
              <Text style={styles.valueText}>{surname}</Text>
            </View>
            <View style={styles.divideLine} />
            <View style={styles.rowField}>
              <Text style={styles.attributeText}>Телефон</Text>
              <Text style={styles.valueText}>{phone_number}</Text>
            </View>
            <View style={styles.divideLine} />
            <View style={styles.rowField}>
              <Text style={styles.attributeText}>Пароль</Text>
              <Text style={styles.valueText}>**********</Text>
            </View>
            <View style={styles.divideLine} />
            <View style={styles.rowField}>
              <Text style={styles.attributeText}>ИНН</Text>
              <Text style={styles.valueText}>{inn}</Text>
            </View>
            <View style={styles.divideLine} />
          </View>
        </View>
        <View style={[styles.component, styles.subscribeInfo]}>
          <View style={styles.headerProfile}>
            <Text style={styles.nameComponentText}>Мои подписки</Text>
          </View>
          <View style={styles.fields}>
            <View style={styles.divideLine} />
            <SubscribeMiniCard />
            <View style={styles.divideLine} />
            <SubscribeMiniCard name_subscribe="Помощь детям" />
            <View style={styles.divideLine} />
          </View>
        </View>

        <View style={[styles.component, styles.helpInfo]}>
          <Text style={styles.helpText}>
            Если вам или вашим знакомым нужна помощь, обращайтесь
          </Text>
          <TouchableOpacity>
            <Text style={styles.applyText}>Обратиться</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.actionButtons}>
          <TouchableOpacity>
            <Text style={styles.actionButtonText}>Выйти из аккаунта</Text>
          </TouchableOpacity>
          <ModalDeteleAccount />
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
  component: {
    backgroundColor: "rgba(255,255,255,1)",
    padding: 20,
    marginHorizontal: 20,
    borderRadius: 20,
    shadowColor: "rgba(36, 27, 79, 0.2)",
    shadowOffset: {
      width: 0,
      height: 0,
    },
    shadowOpacity: 1,
    shadowRadius: 8,
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
  userInfo: { marginTop: 30 },
  headerProfile: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  nameComponentText: {
    fontSize: 16,
    fontFamily: "IBMMedium",
    color: "rgba(113, 113, 113, 1)",
  },
  editButtonText: {
    color: "rgba(22, 3, 111, 1)",
    fontFamily: "IBMMedium",
    fontSize: 12,
  },
  fields: {
    marginTop: 15,
    gap: 10,
  },
  divideLine: {
    width: "100%",
    height: 1,
    backgroundColor: "rgba(237, 236, 240, 1)",
  },
  rowField: {
    flexDirection: "row",
    alignItems: "center",
  },
  attributeText: {
    width: 100,
    color: "rgba(183, 183, 183, 1)",
    fontFamily: "IBMRegular",
    fontSize: 12,
  },
  valueText: {
    fontFamily: "IBMMedium",
    color: "rgba(52, 52, 52, 1)",
  },
  subscribeInfo: {
    marginTop: 15,
  },
  helpInfo: {
    marginTop: 15,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  helpText: {
    width: 190,
    fontSize: 12,
    fontFamily: "IBMMedium",
    color: "rgba(113, 113, 113, 1)",
  },
  applyText: {
    color: "rgba(22, 3, 111, 1)",
    fontFamily: "IBMMedium",
    fontSize: 12,
  },
  actionButtons: {
    alignItems: "center",
    marginTop: 30,
    gap: 15,
    marginBottom: 100,
  },
  actionButtonText: {
    fontFamily: "IBMMedium",
    color: "rgba(113, 113, 113, 1)",
  },
});

export default ProfileScreen;
